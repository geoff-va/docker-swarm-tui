from __future__ import annotations

from typing import Any

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

    async def get_secrets(self) -> list[str]:
        return sorted(list(self.SECRETS.keys()))

    async def get_secret_info(self, secret_id: str) -> dict[str, Any]:
        return self.SECRETS[secret_id]

    async def get_nodes(self) -> list[str]:
        return sorted(list(self.NODES.keys()))
