"""Declarative OData query-option capabilities for collections.

Some Microsoft Graph feeds reject standard OData query options — the
``callRecords`` feed rejects ``$top`` with *"Query option 'Top' is not allowed.
To allow it, set the 'AllowedQueryOptions' property on EnableQueryAttribute or
QueryValidationSettings."* Those named knobs are **server-side** ASP.NET OData
configuration a client cannot change, so the library declares the *exceptions*
on the collection and guards its fluent query-option setters before a request is
sent.

This mirrors the ``@odata`` / ``@limit`` / ``@require_permission`` family: declare
on the model (a ``ClientObjectCollection`` subclass), collect the metadata on the
class, and enforce it at the seam (``top`` / ``skip`` / ``order_by`` / ``filter``
/ ``select`` / ``expand`` — and therefore ``paged`` / ``get_all``).

    >>> from office365.runtime.query_capabilities import query_capabilities
    >>> @query_capabilities(unsupported={"top"}, doc=_DOC)
    ... class CallRecordCollection(EntityCollection[CallRecord]): ...
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Optional

#: Attribute the decorator stamps the :class:`QueryCapability` onto.
_QUERY_CAPABILITY_MARKER = "__query_capability__"
_ON_UNSUPPORTED = ("raise", "warn")


def _normalize(option: str) -> str:
    """Normalize an option name to the ``QueryOptions`` field form (``top``)."""
    return option.strip().lstrip("$").lower().replace("-", "_")


@dataclass(frozen=True)
class QueryCapability:
    """Which OData query options a collection/endpoint accepts.

    ``unsupported`` is a deny-list — the common case, declare only the rejected
    options. ``allowed`` is the inverse allow-list for a feed that accepts a
    fixed set. Only one is set.
    """

    unsupported: frozenset[str] = frozenset()
    allowed: Optional[frozenset[str]] = None
    on_unsupported: str = "raise"
    doc: str = ""
    note: str = ""

    def supports(self, option: str) -> bool:
        """Whether ``option`` (e.g. ``"top"`` or ``"$top"``) is accepted."""
        option = _normalize(option)
        if self.allowed is not None:
            return option in self.allowed
        return option not in self.unsupported


class QueryOptionNotSupportedError(ValueError):
    """Raised when a collection is asked for a query option its endpoint rejects."""

    def __init__(self, owner: type, option: str, capability: QueryCapability) -> None:
        self.owner = owner
        self.option = _normalize(option)
        self.capability = capability
        super().__init__(hint(owner, option, capability))


def hint(owner: type, option: str, capability: QueryCapability) -> str:
    """An actionable message for an unsupported query option."""
    option = _normalize(option)
    text = f"{owner.__name__} does not support ${option}"
    if capability.note:
        text += f" — {capability.note}"
    text += f"; bound the result client-side instead of calling .{option}(...)"
    if capability.doc:
        text += f". See {capability.doc}"
    return text


def _append_doc(target: type, capability: QueryCapability) -> None:
    if capability.allowed is not None:
        declared = f"allowed: {', '.join(sorted(capability.allowed)) or 'none'}"
    else:
        declared = f"unsupported: {', '.join(sorted(capability.unsupported)) or 'none'}"
    target.__doc__ = (target.__doc__ or "") + f"\n    Query options ({declared}).\n"


def query_capabilities(
    *,
    unsupported: Optional[Iterable[str]] = None,
    allowed: Optional[Iterable[str]] = None,
    on_unsupported: str = "raise",
    doc: str = "",
    note: str = "",
) -> Callable[[type], type]:
    """Declare which OData query options a collection class accepts.

    Args:
        unsupported: Options the endpoint rejects (deny-list), e.g. ``{"top"}``.
        allowed: The exact set the endpoint accepts (allow-list). Mutually
            exclusive with ``unsupported``.
        on_unsupported: ``"raise"`` (default) or ``"warn"`` — the latter warns
            and silently ignores the option instead of raising.
        doc: Link to the endpoint documentation.
        note: Extra guidance surfaced in the error or warning.

    Returns:
        A class decorator for a ``ClientObjectCollection`` subclass.
    """
    if unsupported is not None and allowed is not None:
        raise ValueError("pass either unsupported= or allowed=, not both")
    if on_unsupported not in _ON_UNSUPPORTED:
        raise ValueError(f"on_unsupported must be one of {_ON_UNSUPPORTED}, got {on_unsupported!r}")
    capability = QueryCapability(
        unsupported=frozenset(_normalize(option) for option in (unsupported or ())),
        allowed=frozenset(_normalize(option) for option in allowed) if allowed is not None else None,
        on_unsupported=on_unsupported,
        doc=doc,
        note=note,
    )

    def decorator(target: type) -> type:
        if not isinstance(target, type):
            raise TypeError("@query_capabilities applies to a class (a ClientObjectCollection subclass)")
        setattr(target, _QUERY_CAPABILITY_MARKER, capability)
        target._query_capability_decl = capability
        _append_doc(target, capability)
        return target

    return decorator


def query_capabilities_of(target: object) -> Optional[QueryCapability]:
    """The :class:`QueryCapability` declared on a class (or instance), if any."""
    cls = target if isinstance(target, type) else type(target)
    return getattr(cls, "_query_capability_decl", None)


__all__ = [
    "QueryCapability",
    "QueryOptionNotSupportedError",
    "hint",
    "query_capabilities",
    "query_capabilities_of",
]
