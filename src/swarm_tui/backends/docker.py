from __future__ import annotations

import base64
from typing import Any, Literal

import aiodocker
from aiodocker.exceptions import DockerError
from textual import log

from ..exceptions import DockerApiError
from . import models
from .base import BaseBackend


def docker_exc_wrapper(func):
    """Re-Raise DockerError as our DockerApiError"""

    async def _inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DockerError as e:
            raise DockerApiError(e)

    return _inner


class AioDockerBackend(BaseBackend):
    """DockerBackend based on AioHttp"""

    def __init__(self) -> None:
        self._docker: aiodocker.Docker = None

    @property
    def docker(self) -> aiodocker.Docker:
        if self._docker is None:
            self._docker = aiodocker.Docker()
        return self._docker

    @docker_exc_wrapper
    async def get_swarm_info(self) -> dict[str, Any]:
        return dict(await self.docker.swarm.inspect())

    @docker_exc_wrapper
    async def get_secrets(self) -> list[str]:
        result = await self.docker.secrets.list()
        return [item["Spec"]["Name"] for item in result]

    @docker_exc_wrapper
    async def update_secret(
        self,
        secret_id: str,
        labels: dict[str, str] | None = None,
    ) -> bool:
        info = await self.get_secret_info(secret_id)
        version = info["Version"]["Index"]
        return await self.docker.secrets.update(secret_id, version, labels=labels)

    @docker_exc_wrapper
    async def get_secret_info(self, secret_id: str) -> dict[str, Any]:
        return dict(await self.docker.secrets.inspect(secret_id))

    @docker_exc_wrapper
    async def remove_secret(self, secret_id: str) -> bool:
        return await self.docker.secrets.delete(secret_id)

    @docker_exc_wrapper
    async def get_configs(self) -> list[str]:
        result = await self.docker.configs.list()
        return [item["Spec"]["Name"] for item in result]

    @docker_exc_wrapper
    async def get_config_info(self, config_id: str) -> dict[str, Any]:
        result = await self.docker.configs.inspect(config_id)
        return dict(result)

    @docker_exc_wrapper
    async def decode_config_data(self, info: dict[str, Any]) -> str:
        return base64.b64decode(info["Spec"]["Data"]).decode("utf-8")

    @docker_exc_wrapper
    async def get_nodes(self) -> list[models.Node]:
        result = await self.docker.nodes.list()
        return [
            models.Node(hostname=item["Description"]["Hostname"], id=item["ID"])
            for item in result
        ]

    @docker_exc_wrapper
    async def get_node_info(self, node_id: str) -> dict[str, Any]:
        return dict(await self.docker.nodes.inspect(node_id=node_id))

    @docker_exc_wrapper
    async def get_stacks_and_services(
        self,
    ) -> tuple[list[models.Stack], list[models.Service]]:
        # stacks: need to use services.list() and find the ones with a
        # Spec.Labels["com.docker.stack.namespace"]
        # If label dne, not part of stack
        # services - can also get all those at the same time

        # To correlate tasks -> services; task has a ServiceID == service's ID
        # Task # like helloworld.<num> is from the slot
        services_resp = await self.docker.services.list()
        tasks_resp = await self.docker.tasks.list(filters={"desired-state": "running"})

        stacks = {}
        services = {}

        # Populate empty stacks and service objects
        # Stacks key: name, services key: id
        for service in services_resp:
            service_obj = models.Service(
                name=service["Spec"]["Name"], id=service["ID"], tasks=[]
            )

            stack_name = service["Spec"]["Labels"].get("com.docker.stack.namespace")
            if stack_name:
                if stack_name not in stacks:
                    stacks[stack_name] = models.Stack(
                        name=stack_name, id=service["ID"], services=[]
                    )
                # Current service belongs to a stack so add it
                stacks[stack_name].services.append(service_obj)

            # Adds all services initially so we can also add their tasks easilyo
            # since the service object can be shared in the stack services
            services[service_obj.id] = service_obj

        # populate tasks to all services
        for task in tasks_resp:
            service_id = task["ServiceID"]
            if service_id in services:
                services[service_id].tasks.append(
                    models.Task(
                        name=f"{services[service_id].name}.{task['Slot']}",
                        id=task["ID"],
                        state=models.TaskState(task["Status"]["State"]),
                    )
                )
        # Remove services that are part of a stack
        for stack in stacks.values():
            for service in stack.services:
                if service.id in services:
                    services.pop(service.id)

        return list(stacks.values()), list(services.values())

    @docker_exc_wrapper
    async def get_stack_service_info(
        self, node_id: str, node_type: models.DockerNode
    ) -> dict[str, Any]:
        if node_type == models.DockerNodeType.STACK:
            return {"Info": "Docker does not provide stack information"}
        elif node_type == models.DockerNodeType.SERVICE:
            return dict(await self.docker.services.inspect(node_id))
        else:
            return dict(await self.docker.tasks.inspect(node_id))

    @docker_exc_wrapper
    async def get_node_tasks(self, node_id: str) -> list[dict[str, Any]]:
        return []

    async def promote_node(self, node_id: str) -> dict[str, Any]:
        # Get current version of node from nodes endpoint
        # do a node update command with the version and role

        return {}

    async def demote_note(self, node_id: str) -> dict[str, Any]:
        # Get current version of node from nodes endpoint
        # do a node update command with the version and role
        return {}

    async def remove_node(self, node_id: str, force: bool = False) -> dict[str, Any]:
        return dict(await self.docker.nodes.remove(node_id=node_id, force=force))

    async def get_worker_token(self) -> str:
        result = await self.docker.swarm.inspect()
        return result["JoinTokens"]["Worker"]

    async def get_manager_token(self) -> str:
        result = await self.docker.swarm.inspect()
        return result["JoinTokens"]["Manager"]

    async def get_node_join_cmd(self, node_type: Literal["worker", "manager"]) -> str:
        assert node_type in ("worker", "manager")
        if node_type == "worker":
            token = await self.get_worker_token()
        else:
            token = await self.get_manager_token()

        nodes = await self.docker.nodes.list()
        mgr_node = self._find_manager(nodes)
        hostaddr = mgr_node["ManagerStatus"]["Addr"]
        return f"docker swarm join --token {token} {hostaddr}"

    def _find_manager(self, nodes: list[dict[str, Any]]) -> dict[str, Any]:
        """Find a manager node that is reachable; preferably the leader"""
        managers = []
        for node in nodes:
            if node["Spec"]["Role"] == "manager":
                managers.append(node)
                mgr_status = node["ManagerStatus"]
                if mgr_status["Leader"] and mgr_status["Reachability"] == "reachable":
                    return node

        log.info("No reachable leaders found; searching for next reachable manager")
        for node in managers:
            mgr_status = node["ManagerStatus"]
            if mgr_status["Reachability"] == "reachable":
                return node

        raise DockerApiError("No reachable managers found")
