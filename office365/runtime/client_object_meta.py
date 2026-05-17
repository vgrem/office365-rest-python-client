from __future__ import annotations

from typing import Any, Callable, Optional, TypeVar

from office365.runtime.client_object import ClientObject

FuncT = TypeVar("FuncT")


def persist_property(
    property_name: Optional[str] = None,
) -> Callable[[Callable[..., FuncT]], Callable[..., FuncT]]:
    """Decorator to automatically track property access for persistence"""

    def decorator(method: Callable[..., FuncT]) -> Callable[..., FuncT]:
        def wrapper(self: ClientObject, *args: Any, **kwargs: Any) -> FuncT:
            name = property_name if property_name is not None else method.__name__
            if name not in self._properties_to_persist:
                self._properties_to_persist.append(name)
            return method(self, *args, **kwargs)

        return wrapper

    return decorator
