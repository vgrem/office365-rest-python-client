"""Product-agnostic service limits and guardrails.

A :class:`Limit` describes one service limit (value, kind, unit, scope, docs).
The helpers here let call sites *guard-rail* against it — warn, clamp, or raise —
and :func:`bounded` decorates a numeric argument with the same check.

Product packages (e.g. ``office365.sharepoint.thresholds``) declare the concrete
limits; this module only owns the mechanics so the runtime and every product can
share them.
"""

from __future__ import annotations

import inspect
import warnings
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

_ON_EXCEED = ("warn", "raise")

#: A conservative default page/chunk size that stays below SharePoint's 5,000-item
#: list view threshold, so paged reads and imports are safe by default.
SAFE_PAGE_SIZE = 2000

#: Default number of items per OData batch (also SharePoint's bulk-operation limit).
DEFAULT_BATCH_SIZE = 100


class LimitKind(Enum):
    """How strictly a limit is enforced (per Microsoft's definitions)."""

    BOUNDARY = "boundary"  # absolute, can't be exceeded by design
    THRESHOLD = "threshold"  # configurable default
    SUPPORTED = "supported"  # tested value


def _human_bytes(value: int) -> str:
    """Format a byte count as ``250 GB`` when it divides evenly, else ``8,000 bytes``."""
    for suffix, step in (("TB", 1024**4), ("GB", 1024**3), ("MB", 1024**2), ("KB", 1024)):
        if value >= step and value % step == 0:
            return f"{value // step} {suffix}"
    return f"{value:,} bytes"


@dataclass(frozen=True)
class Limit:
    """A single service limit.

    Args:
        name: Human-readable name (e.g. ``"list view threshold"``).
        value: The numeric limit.
        kind: :class:`LimitKind` — boundary / threshold / supported.
        unit: What is counted (``items``, ``bytes``, ``chars``, ``columns``, ...).
        scope: The object it applies to (``list``, ``folder``, ``site``, ...).
        note: Extra guidance surfaced in warnings.
        doc: Link to the authoritative documentation.
    """

    name: str
    value: int
    kind: LimitKind = LimitKind.THRESHOLD
    unit: str = "items"
    scope: str = ""
    note: str = ""
    doc: str = ""

    def __str__(self) -> str:
        if self.unit == "bytes":
            return _human_bytes(self.value)
        return f"{self.value:,} {self.unit}".strip()

    def exceeds(self, value: int) -> bool:
        """Whether ``value`` is over this limit."""
        return value > self.value


class LimitExceededError(ValueError):
    """Raised when a value exceeds a service limit."""

    def __init__(self, limit: Limit, value: int, *, context: str = "") -> None:
        self.limit = limit
        self.value = value
        self.context = context
        super().__init__(hint(limit, context=context, value=value))


def exceeds(limit: Limit, value: int) -> bool:
    """Whether ``value`` is over ``limit``."""
    return limit.exceeds(value)


def hint(limit: Limit, *, context: str = "", value: Optional[int] = None) -> str:
    """An actionable message for a limit, optionally naming the offending value."""
    where = f" for {context}" if context else ""
    if value is None:
        text = f"SharePoint limit '{limit.name}'{where} is {limit}"
    else:
        text = f"{_format_value(limit, value)}{where} exceeds the limit '{limit.name}' ({limit})"
    if limit.note:
        text += f" — {limit.note}"
    if limit.doc:
        text += f" See {limit.doc}"
    return text


def _format_value(limit: Limit, value: int) -> str:
    if limit.unit == "bytes":
        return _human_bytes(value)
    return f"{value:,} {limit.unit}".strip()


def warn_if_exceeds(limit: Limit, value: int, *, context: str = "", stacklevel: int = 3) -> bool:
    """Warn when ``value`` is over ``limit``. Returns whether it warned."""
    if not limit.exceeds(value):
        return False
    warnings.warn(hint(limit, context=context, value=value), UserWarning, stacklevel=stacklevel)
    return True


def ensure_within(
    limit: Limit,
    value: int,
    *,
    context: str = "",
    on_exceed: str = "raise",
) -> None:
    """Enforce ``limit`` for ``value`` — raise :class:`LimitExceededError` or warn.

    Args:
        on_exceed: ``"raise"`` (default) or ``"warn"``.
    """
    if on_exceed not in _ON_EXCEED:
        raise ValueError(f"on_exceed must be one of {_ON_EXCEED}, got {on_exceed!r}")
    if not limit.exceeds(value):
        return
    if on_exceed == "warn":
        warn_if_exceeds(limit, value, context=context, stacklevel=4)
    else:
        raise LimitExceededError(limit, value, context=context)


def bounded(
    arg: str,
    limit: Limit,
    *,
    on_exceed: str = "warn",
    clamp: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Guard a numeric argument against ``limit`` (warn by default).

    A ``None`` argument always passes. With ``clamp=True`` the argument is
    lowered to the limit; otherwise ``on_exceed`` decides between a warning
    (default) and :class:`LimitExceededError`.

    Args:
        arg: Name of the numeric argument (positional or keyword).
        limit: The :class:`Limit` to enforce.
        on_exceed: ``"warn"`` (default) or ``"raise"``.
        clamp: Lower the argument to the limit instead of warning/raising.
    """
    if on_exceed not in _ON_EXCEED:
        raise ValueError(f"on_exceed must be one of {_ON_EXCEED}, got {on_exceed!r}")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        signature = inspect.signature(func)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound = signature.bind_partial(*args, **kwargs)
            value: Any = bound.arguments.get(arg)
            if value is None or not limit.exceeds(value):
                return func(*args, **kwargs)
            if clamp:
                bound.arguments[arg] = limit.value
                return func(*bound.args, **bound.kwargs)
            if on_exceed == "raise":
                raise LimitExceededError(limit, value, context=func.__qualname__)
            warn_if_exceeds(limit, value, context=func.__qualname__, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator
