from __future__ import annotations

from typing import Any, Literal

from . import models


class BaseBackend:
    """Base class for backends"""

    async def get_swarm_info(self) -> dict[str, Any]: ...

    async def get_secrets(self) -> list[str]: ...

    async def get_secret_info(self, secret_id: str) -> dict[str, Any]: ...

    async def remove_secret(self, secret_id: str) -> bool: ...

    async def update_secret(
        self,
        secret_id: str,
        labels: dict[str, str] | None = None,
    ) -> bool: ...

    async def get_configs(self) -> list[str]: ...

    async def get_config_info(self, config_id: str) -> dict[str, Any]: ...

    async def get_stack_service_info(
        self, node_id: str, node_type: models.DockerNode
    ) -> dict[str, Any]: ...

    async def decode_config_data(self, info: dict[str, Any]) -> str: ...

    async def get_nodes(self) -> list[models.Node]: ...

    async def get_stacks_and_services(
        self,
    ) -> tuple[list[models.Stack], list[models.Service]]: ...

    async def get_node_info(self, node_id: str) -> dict[str, Any]: ...

    async def get_node_tasks(self, node_id: str) -> list[dict[str, Any]]: ...

    async def promote_node(self, node_id: str) -> dict[str, Any]: ...

    async def demote_note(self, node_id: str) -> dict[str, Any]: ...

    async def remove_node(
        self, node_id: str, force: bool = False
    ) -> dict[str, Any]: ...

    async def get_worker_token(self) -> str: ...

    async def get_manager_token(self) -> str: ...

    async def get_node_join_cmd(
        self, node_type: Literal["worker", "manager"]
    ) -> str: ...
