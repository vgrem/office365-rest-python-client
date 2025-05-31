from __future__ import annotations

from typing import Any, Callable, Optional

from office365.runtime.client_object import ClientObject, PropertyT


def persist_property(property_name=None):
    # type: (Optional[str]) -> Callable[[Callable[..., PropertyT]], Callable[..., PropertyT]]
    """Decorator to automatically track property access for persistence"""

    def decorator(method):
        # type: (Callable[..., PropertyT]) -> Callable[..., PropertyT]
        def wrapper(self, *args, **kwargs):
            # type: (ClientObject, *Any, **Any) -> PropertyT
            name = property_name if property_name is not None else method.__name__
            if name not in self._properties_to_persist:
                self._properties_to_persist.append(name)
            return method(self, *args, **kwargs)

        return wrapper

    return decorator
