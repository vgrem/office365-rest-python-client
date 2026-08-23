"""CSV exporter for ClientObjectCollection — reuses .select() + .expand()."""

from __future__ import annotations

import csv
from typing import IO, TYPE_CHECKING, Any, List, Optional

from office365.runtime.client_object_collection import ClientObjectCollection

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject


def write_csv(collection: ClientObjectCollection, file: IO[str]) -> None:
    """Write collection items to CSV using query_options.select + .expand.

    When no ``.select()`` is set, all item properties are exported.
    Plain select fields (e.g. ``"displayName"``) produce one column.
    Dotted select fields (e.g. ``"members/displayName"``) walk into an
    expanded navigation property — one CSV row is emitted per child item.
    Dotted fields must reference a single navigation property.

    Usage:
        >>> collection.get_all() \\
        ...     .select(["displayName", "members/displayName", "members/email"]) \\
        ...     .expand(["members"]) \\
        ...     .to_csv(f) \\
        ...     .execute_query()
    """
    items = list(collection)
    if not items:
        return

    select = collection.query_options.select
    if not select:
        select = sorted({key for item in items for key in item.properties.keys()})
    expand = set(collection.query_options.expand)
    dotted = [f.split("/", 1) for f in select if "/" in f]
    navs = {nav for nav, _ in dotted}
    if len(navs) > 1:
        raise ValueError(
            f"CSV export supports dotted select fields on a single navigation property, got: {sorted(navs)}"
        )
    nav = next(iter(navs), None)

    plain = [f for f in select if "/" not in f]
    w = csv.writer(file)
    w.writerow(select)

    for item in items:
        children = _resolve_property(item, nav, expand)
        base = [str(item.properties.get(k, "")) for k in plain]
        for child in children:
            row = list(base)
            for _nav_prop, field_name in dotted:
                row.append(_property_value(child, field_name))
            w.writerow(row)


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


def _property_value(prop: "dict | ClientObject", field_name: str) -> str:
    """Read a property value from an item that may be a ClientObject or dict."""
    if isinstance(prop, dict):
        return str(prop.get(field_name, ""))
    return str(prop.properties.get(field_name, ""))


def write_records(records: list[dict], file: IO[str], columns: Optional[List[str]] = None) -> None:
    """Write a list of dict records to CSV.

    Args:
        records: Rows as dicts (one dict per line).
        file: Writable text stream.
        columns: Explicit column order; defaults to the union of record keys
            in first-appearance order.
    """
    if not records:
        return
    if columns is None:
        columns = list(dict.fromkeys(key for record in records for key in record))
    writer = csv.writer(file)
    writer.writerow(columns)
    for record in records:
        writer.writerow(["" if record.get(key) is None else str(record.get(key)) for key in columns])
