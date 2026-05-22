from __future__ import annotations

import logging
import threading
from collections.abc import Callable, Iterator
from typing import Generic

from typing_extensions import ParamSpec, Self

logger = logging.getLogger(__name__)

P = ParamSpec("P")


class EventHandler(Generic[P]):
    """A thread-safe, type-safe event handler.
    Usage::

        on_change: EventHandler[[str, int]] = EventHandler()
        on_change += lambda name, value: print(name, value)
        on_change("x", 42)  # type-checked call
        on_change.notify("x", 42)  # explicit form

    Args:
        once: If True, each listener fires once then auto-removes.
    """

    def __init__(self, once: bool = False) -> None:
        self._listeners: list[Callable[P, None]] = []
        self._once = once
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Collection protocol
    # ------------------------------------------------------------------ #

    def __contains__(self, listener: Callable[P, None]) -> bool:
        with self._lock:
            return listener in self._listeners

    def __iter__(self) -> Iterator[Callable[P, None]]:
        with self._lock:
            snapshot = list(self._listeners)  # snapshot: safe for concurrent notify
        return iter(snapshot)

    def __len__(self) -> int:
        with self._lock:
            return len(self._listeners)

    def __repr__(self) -> str:
        return f"EventHandler(listeners={len(self)}, once={self._once})"

    # ------------------------------------------------------------------ #
    # Subscription operators
    # ------------------------------------------------------------------ #

    def __iadd__(self, listener: Callable[P, None]) -> Self:
        """Add a listener: ``handler += callback``."""
        if not callable(listener):
            raise TypeError(f"Listener must be callable, got {type(listener)!r}")
        with self._lock:
            self._listeners.append(listener)
        return self

    def __isub__(self, listener: Callable[P, None]) -> Self:
        """Remove a listener: ``handler -= callback``.

        Silently ignores missing listeners (discard semantics).
        Use ``remove(strict=True)`` if you need a ValueError on missing.
        """
        with self._lock:
            try:
                self._listeners.remove(listener)
            except ValueError:
                pass
        return self

    # ------------------------------------------------------------------ #
    # Notification
    # ------------------------------------------------------------------ #

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Self:
        """Callable interface -- delegates to notify()."""
        return self.notify(*args, **kwargs)

    def notify(self, *args: P.args, **kwargs: P.kwargs) -> Self:
        """Fire all registered listeners.

        Thread-safe: takes a snapshot before iterating so that listeners
        added or removed during notification don't affect this call.
        """
        with self._lock:
            snapshot = list(self._listeners)
            if self._once:
                self._listeners.clear()

        for listener in snapshot:
            try:
                listener(*args, **kwargs)
            except Exception:
                logger.exception("Unhandled exception in listener %r", listener)

        return self

    # ------------------------------------------------------------------ #
    # Explicit helpers
    # ------------------------------------------------------------------ #

    def remove(self, listener: Callable[P, None], *, strict: bool = False) -> Self:
        """Explicit remove with optional strict mode.

        Args:
            listener: The callable to remove.
            strict:   If True, raises ValueError when listener is not found.
        """
        with self._lock:
            try:
                self._listeners.remove(listener)
            except ValueError:
                if strict:
                    raise
        return self

    def clear(self) -> Self:
        """Remove all listeners."""
        with self._lock:
            self._listeners.clear()
        return self
