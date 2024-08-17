from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DockerNodeType(Enum):
    TASK = "task"
    SERVICE = "service"
    STACK = "stack"


@dataclass
class Secret:
    name: str
    data: str


@dataclass
class Config:
    name: str
    data: str


@dataclass
class Node:
    name: str
    server: str


class DockerNode:
    node_type: DockerNodeType


@dataclass
class Task(DockerNode):
    name: str
    node_type: DockerNodeType = DockerNodeType.TASK


@dataclass
class Service(DockerNode):
    name: str
    tasks: list[Task]
    node_type: DockerNodeType = DockerNodeType.SERVICE


@dataclass
class Stack(DockerNode):
    name: str
    services: list[Service]
    node_type: DockerNodeType = DockerNodeType.STACK
