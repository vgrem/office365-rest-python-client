import types
from typing import Any, Callable, Generic, Iterator, List, TypeVar, Union

from typing_extensions import Self

F = TypeVar("F", bound=Callable[..., None])


class EventHandler(Generic[F]):
    """A lightweight event handler with Pythonic notification patterns.

    Features:
    - Supports both direct call (`__call__`) and explicit `notify()`
    - Clean automatic removal of one-time handlers
    - Detailed error logging
    - Type-safe operations
    - Method chaining support

    Usage:
        # Traditional style
        handler = EventHandler()
        handler += callback
        handler.notify(args)

        # Pythonic callable style
        handler = EventHandler()
        handler += callback
        handler(args)
    """

    def __init__(self, once: bool = False) -> None:
        """Initialize the event handler.

        Args:
            once: If True, handlers auto-remove after first notification
        """
        self._listeners: List[F] = []
        self._once = once

    def __contains__(self, listener: F) -> bool:
        return listener in self._listeners

    def __iter__(self) -> Iterator[F]:
        return iter(self._listeners)

    def __iadd__(self, listener: F) -> Self:
        """Add listener with += operator."""
        if not callable(listener):
            raise TypeError("Listener must be callable")
        self._listeners.append(listener)
        return self

    def __isub__(self, listener: F) -> Self:
        """Remove listener with -= operator."""
        self._listeners.remove(listener)
        return self

    def __len__(self):
        return len(self._listeners)

    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        """Call interface that delegates to notify()."""
        return self.notify(*args, **kwargs)

    def __repr__(self) -> str:
        return f"EventHandler(listeners={len(self)}, once={self._once})"

    def clear(self) -> Self:
        """Remove all listeners"""
        self._listeners.clear()
        return self

    def notify(self, *args: Any, **kwargs: Any) -> Self:
        """Notify all registered listeners.

        Args:
            *args: Positional arguments for listeners
            **kwargs: Keyword arguments for listeners

        Returns:
            Self for method chaining
        """
        for listener in self._listeners[:]:
            if self._once:
                self._listeners.remove(listener)
            listener(*args, **kwargs)
        return self

    @staticmethod
    def is_system(listener):
        # type: (F) -> bool
        from office365.runtime.client_request import ClientRequest
        from office365.runtime.client_runtime_context import ClientRuntimeContext

        if isinstance(listener, types.MethodType):
            return isinstance(listener.__self__, (ClientRequest, ClientRuntimeContext))
        if isinstance(listener, types.FunctionType):
            return listener.__module__ == ClientRuntimeContext.__module__
        else:
            raise ValueError("Invalid listener type")
