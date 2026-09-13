"""OData metadata type names -> generated client classes (codegen side)."""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from functools import lru_cache
from typing import Optional, Sequence, Type

from generator.builders.type_mapping import client_type_name


class ClientTypeResolver:
    """Maps OData metadata type names to their generated Python classes."""

    def __init__(self, modules: Sequence[str]) -> None:
        self._modules_key = tuple(sorted(m.strip() for m in modules if m and m.strip()))

    def resolve(self, type_name: str | None) -> Optional[Type]:
        """Resolves an OData type name (e.g. ``SP.Web``) to its Python class."""
        if not type_name:
            return None
        return _resolve_cached(client_type_name(type_name), self._modules_key)

    @staticmethod
    def cache_clear() -> None:
        """Clears the shared resolution cache."""
        _resolve_cached.cache_clear()


@lru_cache(maxsize=1024)
def _resolve_cached(target_name: str, modules_key: tuple[str, ...]) -> Optional[Type]:
    """Searches the configured module roots for a class named ``target_name``."""

    def _search_module(module_name: str) -> Optional[Type]:
        try:
            module = importlib.import_module(module_name)

            if hasattr(module, target_name):
                cls = getattr(module, target_name)
                if inspect.isclass(cls):
                    return cls

            if hasattr(module, "__path__"):
                for _, name, _ in pkgutil.iter_modules(module.__path__):
                    found = _search_module(module_name + "." + name)
                    if found:
                        return found

        except (ImportError, AttributeError):
            pass
        return None

    for module_name in modules_key:
        result = _search_module(module_name)
        if result:
            return result
    return None
