from __future__ import annotations

import base64
from typing import Any, cast

import aiodocker
from textual import log

from . import models
from .base import BaseBackend


class AioDockerBackend(BaseBackend):
    """DockerBackend based on AioHttp"""

    def __init__(self) -> None:
        self._docker: aiodocker.Docker = None

    @property
    def docker(self) -> aiodocker.Docker:
        if self._docker is None:
            self._docker = aiodocker.Docker()
        return self._docker

    async def get_secrets(self) -> list[str]:
        result = await self.docker.secrets.list()
        return [item["Spec"]["Name"] for item in result]

    async def get_secret_info(self, secret_id: str) -> dict[str, Any]:
        return dict(await self.docker.secrets.inspect(secret_id))

    async def get_configs(self) -> list[str]:
        result = await self.docker.configs.list()
        return [item["Spec"]["Name"] for item in result]

    async def get_config_info(self, config_id: str) -> dict[str, Any]:
        result = await self.docker.configs.inspect(config_id)
        return dict(result)

    async def decode_config_data(self, data: str) -> str:
        return base64.b64decode(data).decode("utf-8")

    async def get_nodes(self) -> list[models.Node]:
        result = await self.docker.nodes.list()
        return [
            models.Node(hostname=item["Description"]["Hostname"], id=item["ID"])
            for item in result
        ]

    async def get_node_info(self, node_id: str) -> dict[str, Any]:
        return dict(await self.docker.nodes.inspect(node_id=node_id))

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

    async def get_node_tasks(self, node_id: str) -> list[dict[str, Any]]:
        return []
