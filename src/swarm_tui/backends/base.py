from __future__ import annotations

from typing import Any, Mapping

from . import models


class BaseBackend:
    """Base class for backends"""

    async def get_secrets(self) -> list[str]: ...

    async def get_secret_info(self, secret_id: str) -> dict[str, Any]: ...

    async def get_configs(self) -> list[str]: ...

    async def get_config_info(self, config_id: str) -> dict[str, Any]: ...

    async def decode_config_data(self, data: str) -> str: ...

    async def get_nodes(self) -> list[str]: ...

    async def get_stacks_and_services(
        self,
    ) -> tuple[list[models.Stack], list[models.Service]]: ...

    async def get_node_info(
        self, node_id: str, node_type: models.DockerNodeType
    ) -> dict[str, Any]: ...

    async def get_node_tasks(self, node_id: str) -> list[dict[str, Any]]: ...
