from __future__ import annotations

from typing import Any

from . import models
from .base import BaseBackend


class FakeBackend(BaseBackend):
    """A backend producing some fake data"""

    STACK_INFO: dict[str, Any] = {"stack 1": "Stack 1 Info", "stack 2": "Stack 2 Info"}
    SERVICE_INFO: dict[str, Any] = {
        "service 1": "Service 1 Info",
        "service 2": "Service 2 Info",
        "service 3": "Service 3 Info",
        "service 4": "Service 3 Info",
    }
    TASK_INFO: dict[str, Any] = {
        "task.1": "Task 1 Info",
        "task.2": "Task 2 Info",
        "task.3": "Task 3 Info",
        "task.4": "Task 4 Info",
    }

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

    NODES = {
        "manager 1": {
            "ID": "7yzl92x79aoyfc2sjpnr8wfsn",
            "Version": {"Index": 15996},
            "CreatedAt": "2024-03-19T21:12:44.287483594Z",
            "UpdatedAt": "2024-08-17T06:14:52.975264179Z",
            "Spec": {"Labels": {}, "Role": "manager", "Availability": "active"},
            "Description": {
                "Hostname": "docker-desktop",
                "Platform": {"Architecture": "aarch64", "OS": "linux"},
                "Resources": {"NanoCPUs": 8000000000, "MemoryBytes": 8222203904},
                "Engine": {
                    "EngineVersion": "25.0.3",
                    "Plugins": [
                        {"Type": "Log", "Name": "awslogs"},
                        {"Type": "Log", "Name": "fluentd"},
                        {"Type": "Log", "Name": "gcplogs"},
                        {"Type": "Log", "Name": "gelf"},
                        {"Type": "Log", "Name": "journald"},
                        {"Type": "Log", "Name": "json-file"},
                        {"Type": "Log", "Name": "local"},
                        {"Type": "Log", "Name": "splunk"},
                        {"Type": "Log", "Name": "syslog"},
                        {"Type": "Network", "Name": "bridge"},
                        {"Type": "Network", "Name": "host"},
                        {"Type": "Network", "Name": "ipvlan"},
                        {"Type": "Network", "Name": "macvlan"},
                        {"Type": "Network", "Name": "null"},
                        {"Type": "Network", "Name": "overlay"},
                        {"Type": "Volume", "Name": "local"},
                    ],
                },
                "TLSInfo": {
                    "TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUA2/2id0OMJZLuhQoVbjvCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMjQwMzE5MjEwODAwWhcNNDQwMzE0MjEw\nODAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABH+gbdj92lJBxErHquMvLjsBUd/W03u/HGsu3K8d4nO1hoZO+SUrO7dkyC1F\nUnCaUd5mw4RAlnKx3ioR0PqmfFyjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBTCw7enWgmQUcsVLQMGae8UuqRiYjAKBggqhkjO\nPQQDAgNIADBFAiADn5XfGji8NA1qZa2PVoq23L/8qIrfC7FvyT2VQB3WKAIhALA2\nJffrJOb6SzasmrQLEFTjlllo9QaPfJpqYIDfT+E7\n-----END CERTIFICATE-----\n",
                    "CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLh",
                    "CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZQcDQgAEf6Bt2P3aUkHESseq4y8uOwFR39bTe78cay7crx3ic7WGhk75JSs7t2TILUVScJpR3mbDhECWcrHeKhHQ+qZ8XA==",
                },
            },
            "Status": {"State": "ready", "Addr": "192.168.65.3"},
            "ManagerStatus": {
                "Leader": True,
                "Reachability": "reachable",
                "Addr": "192.168.65.3:2377",
            },
        },
        "worker 1": {"other": "stuff..."},
    }
    CONFIGS = {
        "config 1": {"heres": {"some": "nested"}, "keys": "!!!"},
        "config 2": {"a": "b"},
        "config 3": {"c": "d", "e": "f"},
    }
    STACKS = [
        models.Stack(
            "stack 1",
            id="stack.1",
            services=[
                models.Service(
                    "service 1",
                    id="stack1.service1",
                    tasks=[
                        models.Task("task.1", id="stack1.service1.task1"),
                        models.Task("task.2", id="stack1.service1.task2"),
                    ],
                ),
                models.Service(
                    "service 2",
                    id="stack1.service2",
                    tasks=[
                        models.Task("task.1", id="stack1.service2.task1"),
                        models.Task("task.2", id="stack1.service2.task2"),
                    ],
                ),
            ],
        ),
        models.Stack(
            "stack 2",
            id="stack2",
            services=[
                models.Service(
                    "service 1",
                    id="stack2.service1",
                    tasks=[
                        models.Task("task1.", id="stack2.service1.task1"),
                        models.Task("task2.", id="stack2.service1.task2"),
                    ],
                )
            ],
        ),
    ]
    SERVICES = [
        models.Service(
            "service 3",
            id="service3",
            tasks=[
                models.Task("task.1", id="service3.task1"),
                models.Task("task.2", id="service3.task2"),
            ],
        ),
        models.Service(
            "service 4",
            id="service4",
            tasks=[
                models.Task("task.1", id="servic4.task1"),
                models.Task("task.2", id="servic4.task2"),
                models.Task("task.3", id="servic4.task3"),
            ],
        ),
    ]

    async def get_secrets(self) -> list[str]:
        return sorted(list(self.SECRETS.keys()))

    async def get_secret_info(self, secret_id: str) -> dict[str, Any]:
        return self.SECRETS.get(secret_id, {})

    async def get_nodes(self) -> list[str]:
        return sorted(list(self.NODES.keys()))

    async def get_node_info(self, node_id: str) -> dict[str, Any]:
        return self.NODES.get(node_id, {})

    async def get_stack_service_info(
        self, node_id: str, node_type: models.DockerNodeType
    ) -> dict[str, Any]:
        if node_type == models.DockerNodeType.STACK:
            return self.STACK_INFO.get(node_id, "")
        if node_type == models.DockerNodeType.SERVICE:
            return self.SERVICE_INFO.get(node_id, "")
        if node_type == models.DockerNodeType.TASK:
            return self.TASK_INFO.get(node_id, "")

    async def get_configs(self) -> list[str]:
        return sorted(list(self.CONFIGS.keys()))

    async def get_config_info(self, config_id: str) -> dict[str, Any]:
        return self.CONFIGS.get(config_id, {})

    async def get_stacks_and_services(
        self,
    ) -> tuple[list[models.Stack], list[models.Service]]:
        return self.STACKS, self.SERVICES
