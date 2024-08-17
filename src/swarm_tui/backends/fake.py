from __future__ import annotations

from typing import Any

from . import models
from .base import BaseBackend


class FakeBackend(BaseBackend):
    """A backend producing some fake data"""

    SECRETS = {
        "short": {
            "ID": "lps6ujo3s56qewv4uz4cbprm5",
            "Version": {"Index": 13408},
            "CreatedAt": "2024-08-16T21:51:58.582485264Z",
            "UpdatedAt": "2024-08-16T21:51:58.582485264Z",
            "Spec": {"Name": "short", "Labels": {}},
        },
        "this-is-a-longer-secret-name": {
            "ID": "bieo30psi8basb23r0dnzbwqo",
            "Version": {"Index": 13409},
            "CreatedAt": "2024-08-16T21:51:58.582485264Z",
            "UpdatedAt": "2024-08-16T21:51:58.582485264Z",
            "Spec": {"Name": "this-is-a-longer-secret-name", "Labels": {}},
        },
        "maybe-average-ish": {
            "ID": "lkiux35zanvgh2oijsp2mdhua",
            "Version": {"Index": 13410},
            "CreatedAt": "2024-08-16T21:51:58.582485264Z",
            "UpdatedAt": "2024-08-16T21:51:58.582485264Z",
            "Spec": {"Name": "maybe-average-ish", "Labels": {}},
        },
    }

    NODES = {"manager 1": {}, "worker 1": {}}
    CONFIGS = {"config 1": {}, "config 2": {}, "config 3": {}}
    STACKS = [
        models.Stack(
            "stack 1",
            services=[
                models.Service(
                    "service 1",
                    tasks=[models.Task("task.1"), models.Task("task.2")],
                ),
                models.Service(
                    "service 2",
                    tasks=[models.Task("task.1"), models.Task("task.2")],
                ),
            ],
        ),
        models.Stack(
            "stack 2",
            services=[
                models.Service(
                    "service 1",
                    tasks=[models.Task("task.1"), models.Task("task.2")],
                )
            ],
        ),
    ]
    SERVICES = [
        models.Service(
            "service 3",
            tasks=[models.Task("task.1"), models.Task("task.2")],
        ),
        models.Service(
            "service 4",
            tasks=[models.Task("task.1"), models.Task("task.2"), models.Task("task.3")],
        ),
    ]

    async def get_secrets(self) -> list[str]:
        return sorted(list(self.SECRETS.keys()))

    async def get_secret_info(self, secret_id: str) -> dict[str, Any]:
        return self.SECRETS[secret_id]

    async def get_nodes(self) -> list[str]:
        return sorted(list(self.NODES.keys()))

    async def get_configs(self) -> list[str]:
        return sorted(list(self.CONFIGS.keys()))

    async def get_stacks_and_services(
        self,
    ) -> tuple[list[models.Stack], list[models.Service]]:
        return self.STACKS, self.SERVICES
