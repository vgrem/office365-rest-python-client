from __future__ import annotations

from dataclasses import dataclass

_ODATA_MARKER = "__odata__"


@dataclass
class ODataPropertyMeta:
    name: str
    persist: bool = False
    filterable: bool = False
    nullable: bool = True
    sortable: bool = False
    searchable: bool = False
    description: str = ""


def odata(name: str, **attrs: bool | str):
    """Declare OData metadata for a property.

    Args:
        name: The JSON key name in the Graph API response.
        **attrs: Optional attributes (persist, filterable, nullable, ...)
    """

    def decorator(method):
        meta = ODataPropertyMeta(name=name, **attrs)  # type: ignore[arg-type]
        target = method.fget if isinstance(method, property) else method
        setattr(target, _ODATA_MARKER, meta)
        return method

    return decorator
