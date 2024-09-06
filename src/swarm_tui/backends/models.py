from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# FIX: Not really a docker node type, better class name
class DockerNodeType(Enum):
    TASK = "task"
    SERVICE = "service"
    STACK = "stack"


class TaskState(Enum):
    """Valid states for a swarm Task

    Shown in order they move through
    """

    NEW = "new"
    PENDING = "pending"
    ASSIGNED = "assigned"
    ACCEPTED = "accepted"
    READY = "ready"
    PREPARING = "preparing"
    STARTING = "starting"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    SHUTDOWN = "shutdown"
    REJECTED = "rejected"
    ORPHANED = "orphaned"
    REMOVE = "remove"


@dataclass
class Secret:
    id: str
    name: str


@dataclass
class Config:
    name: str
    data: str


@dataclass
class Node:
    hostname: str
    id: str


class DockerNode:
    node_type: DockerNodeType


@dataclass
class Task(DockerNode):
    name: str
    id: str
    node_type: DockerNodeType = DockerNodeType.TASK
    state: TaskState = TaskState.NEW


@dataclass
class Service(DockerNode):
    name: str
    id: str
    tasks: list[Task]
    node_type: DockerNodeType = DockerNodeType.SERVICE


@dataclass
class Stack(DockerNode):
    name: str
    id: str
    services: list[Service]
    node_type: DockerNodeType = DockerNodeType.STACK
