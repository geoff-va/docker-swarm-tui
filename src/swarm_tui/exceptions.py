from __future__ import annotations


class SwarmTuiError(Exception):
    """Base Exception"""


class DockerApiError(SwarmTuiError):
    """Error in Docker API"""
