from __future__ import annotations

from dataclasses import dataclass


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
    pass


@dataclass
class Task(DockerNode):
    name: str


@dataclass
class Service(DockerNode):
    name: str
    tasks: list[Task]


@dataclass
class Stack(DockerNode):
    name: str
    services: list[Service]
