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


@dataclass
class Task:
    name: str


@dataclass
class Service:
    name: str
    tasks: list[Task]


@dataclass
class Stack:
    name: str
    services: list[Service]
