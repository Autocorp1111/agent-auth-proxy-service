"""
Dependency injection for Agent Auth Proxy
"""

from fastapi import Request

from app.bitwarden import BitwardenClient


def get_bitwarden_client(request: Request) -> BitwardenClient:
    return request.app.state.bitwarden