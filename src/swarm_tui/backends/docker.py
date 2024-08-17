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
        return [], []

    async def get_node_tasks(self, node_id: str) -> list[dict[str, Any]]:
        return []
