from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Dict, Generic

from typing_extensions import Self

from office365.runtime.client_object import T


def mapped_property(name: str) -> Callable:
    """
    Decorator that maps a property to a specific key in _properties

    Args:
        name: The key to use when storing in _properties dictionary
    """

    def decorator(func: Callable) -> property:
        @wraps(func)
        def wrapper(self: Any) -> Any:
            value = func(self)
            if hasattr(self, "_properties"):
                self._properties[name] = value
            return value

        wrapper._serialized = True
        return property(wrapper)

    return decorator


class BaseScanner(ABC, Generic[T]):
    def __init__(self, source: T) -> None:
        self.source = source
        self._properties: Dict[str, Any] = {}

    @abstractmethod
    def build_query(self) -> Self:
        pass

    def scan(self) -> Self:
        self.build_query()
        self.source.execute_query()
        self.process()
        return self

    def process(self) -> None:
        for name, attr in self.__class__.__dict__.items():
            if isinstance(attr, property) and hasattr(attr.fget, "_serialized"):
                getattr(self, name)

    @property
    def properties(self):
        return self._properties

    def __repr__(self):
        return f"{self.__class__.__name__}({self._properties})"
