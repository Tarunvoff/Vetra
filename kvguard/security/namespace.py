"""Tenant namespace governance."""

from typing import Dict, Optional
from kvguard.core.models import CacheNamespace


class NamespaceManager:
    """Manages cache namespaces within tenants."""

    def __init__(self) -> None:
        self._namespaces: Dict[str, CacheNamespace] = {
            "default": CacheNamespace(
                namespace_id="default",
                tenant_id="default",
                description="Default public system namespace",
                is_public=True,
            )
        }

    def register_namespace(self, namespace: CacheNamespace) -> None:
        self._namespaces[namespace.namespace_id] = namespace

    def get_namespace(self, namespace_id: str) -> Optional[CacheNamespace]:
        return self._namespaces.get(namespace_id)
