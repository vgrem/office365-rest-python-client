"""Record projection — turns a loaded collection into plain dict records.

This is the shared extension point for every tabular exporter (CSV, pandas,
future formats). Format-specific writers consume ``iter_records`` and apply
their own value coercion on top of the native, JSON-safe values produced here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.converters.value import serialize_value

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject


def iter_records(collection: "ClientObjectCollection") -> List[Dict[str, Any]]:
    """Project a loaded collection into plain dict records.

    Mirrors ``csv_writer.write_csv``: plain select fields become columns,
    dotted select fields (e.g. ``"members/displayName"``) walk into a single
    expanded navigation property — one record is emitted per child item.
    When no ``.select()`` is set, all item properties are exported (sorted).

    Every selected key is emitted (``None``-filled when absent) so column order
    and headers are stable across formats.

    Args:
        collection: A loaded collection (items populated after execute_query()).

    Raises:
        ValueError: When dotted select fields reference more than one navigation
            property.
    """
    items = list(collection)
    if not items:
        return []

    select = collection.query_options.select
    if not select:
        select = sorted({key for item in items for key in item.properties.keys()})
    expand = set(collection.query_options.expand)
    dotted = [field.split("/", 1) for field in select if "/" in field]
    navs = {nav for nav, _ in dotted}
    if len(navs) > 1:
        raise ValueError(
            f"Record export supports dotted select fields on a single navigation property, got: {sorted(navs)}"
        )
    nav = next(iter(navs), None)
    plain = [field for field in select if "/" not in field]

    records: List[Dict[str, Any]] = []
    for item in items:
        children = _resolve_property(item, nav, expand)
        base: Dict[str, Any] = {key: serialize_value(item.properties.get(key)) for key in plain}
        for child in children:
            record = dict(base)
            for _nav_prop, field_name in dotted:
                record[f"{_nav_prop}/{field_name}"] = _property_value(child, field_name)
            records.append(record)
    return records


def _resolve_property(item: "ClientObject", nav: str | None, expand: set[str]) -> list[Any]:
    """Resolve an expanded navigation property into a list of child items."""
    if nav is None or nav not in expand:
        return [{}]
    raw = item.properties.get(nav)
    if raw is None:
        return [{}]
    if isinstance(raw, ClientObjectCollection):
        return list(raw) or [{}]
    return [raw]


def _property_value(prop: "dict | ClientObject", field_name: str) -> Any:
    """Read a property value from an item that may be a ClientObject or dict."""
    if isinstance(prop, dict):
        return serialize_value(prop.get(field_name))
    return serialize_value(prop.properties.get(field_name))
