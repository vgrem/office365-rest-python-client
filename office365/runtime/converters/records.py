"""Record projection — turns a loaded collection into plain dict records.

This is the shared extension point for every tabular exporter (CSV, pandas,
future formats). Format-specific writers consume ``iter_records`` and apply
their own value coercion on top of the native, JSON-safe values produced here.

The column set is the *type's*, not the page's: a row of a model should carry the
same names the serializer, ``$select`` and the migration imports use, or every
exporter re-derives them for itself.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.converters.value import serialize_value
from office365.runtime.schema import TypeSchema
from office365.runtime.types.odata_property import request_version

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject


def iter_records(
    collection: "ClientObjectCollection", raw: bool = False, rows_from: str | None = None
) -> List[Dict[str, Any]]:
    """Project a loaded collection into plain dict records.

    Mirrors ``csv_writer.write_csv``: plain select fields become columns,
    dotted select fields (e.g. ``"members/displayName"``) walk into a single
    expanded navigation property — one record is emitted per child item.
    When no ``.select()`` is set, the type's declared columns are exported, in
    declaration order (see :func:`declared_columns`).

    ``rows_from`` names a collection-valued property to fan out over *without* a
    dotted select — the case Graph leaves no projection for: ``assignedLicenses``
    is a complex collection, so ``$expand`` is refused ("not a navigation
    property") and ``$select=assignedLicenses/skuId`` is refused ("invalid
    property"). The property is selected and each child becomes a row, with the
    child's own properties as columns.

    Every selected key is emitted (``None``-filled when absent) so column order
    and headers are stable across formats.

    Args:
        collection: A loaded collection (items populated after execute_query()).
        raw: When True, keep native property values (skip ``serialize_value``
            coercion) — used for lossless round-trips like the migration toolkit.
        rows_from: Name of a collection-valued property to emit one record per
            child of, instead of one record per item.

    Raises:
        ValueError: When dotted select fields reference more than one navigation
            property, or when ``rows_from`` is combined with them or with a
            projection that names no column to carry.
    """
    return records_from_items(
        list(collection),
        collection.query_options.select,
        collection.query_options.expand,
        raw=raw,
        rows_from=rows_from,
    )


def declared_columns(items: List["ClientObject"]) -> List[str]:
    """The columns of these items: the type's declarations, then the rest of the page.

    The response used to answer this question — the keys one page happened to carry,
    sorted — which made the column set and its order a property of the *page*: an
    item carrying an extra field reordered every header, and a declared column the
    service left out of a page vanished instead of arriving empty. ``TypeSchema.columns``
    is that question answered by the model, spelled as the client's own service root
    spells it (a stable client exports no preview column), so those names come first,
    in declaration order.

    A name the metadata does not describe still follows, sorted, rather than being
    dropped: a list item's site columns exist on the wire and not in the CSDL, and an
    exporter that silently lost them would be the lossy one. The whole candidate list
    goes through one :meth:`TypeSchema.projection`, so a name the client's root does
    not declare is dropped whether the model declares it or the page merely carried it.
    """
    model = type(items[0])
    declared = TypeSchema.of(model).columns
    carried = {key for item in items for key in item.properties.keys()}
    return model._schema.projection(
        [*declared, *sorted(carried.difference(declared))], request_version(items[0].context)
    )


def records_from_items(
    items: List["ClientObject"],
    select: List[str],
    expand: "set[str] | list[str]",
    raw: bool = False,
    rows_from: str | None = None,
) -> List[Dict[str, Any]]:
    """Project a list of loaded items into records (the page-level primitive).

    Used by :func:`iter_records` and by the paged (streaming) exporter, so a
    large collection can be exported page by page without materializing it all.
    """
    if not items:
        return []
    select = list(select) if select else declared_columns(items)
    expand = set(expand)
    dotted = [field.split("/", 1) for field in select if "/" in field]
    navs = {nav for nav, _ in dotted}
    if len(navs) > 1:
        raise ValueError(
            f"Record export supports dotted select fields on a single navigation property, got: {sorted(navs)}"
        )
    if rows_from:
        return _rows_from_children(items, select, rows_from, dotted, raw)
    nav = next(iter(navs), None)
    plain = [field for field in select if "/" not in field]

    records: List[Dict[str, Any]] = []
    for item in items:
        children = _resolve_property(item, nav, expand)
        base: Dict[str, Any] = {key: _value(item.properties.get(key), raw) for key in plain}
        for child in children:
            record = dict(base)
            for _nav_prop, field_name in dotted:
                record[f"{_nav_prop}/{field_name}"] = _property_value(child, field_name, raw)
            records.append(record)
    return records


def _rows_from_children(
    items: List["ClientObject"], select: List[str], rows_from: str, dotted: List[List[str]], raw: bool
) -> List[Dict[str, Any]]:
    """One record per child of ``rows_from``, with the child's own columns.

    A child's columns are the fields its type declares, in declaration order, so a
    record says ``skuId`` rather than the guessed ``assignedLicenses/skuId`` that
    ``$select`` would have named — Graph refuses to name a child field at all. A
    field that happens to be empty is still a column: a licence with no disabled
    plan writes an empty cell, not a shorter row.
    """
    if dotted:
        raise ValueError("rows_from fans out over a property; it cannot be combined with dotted select fields")
    plain = [field for field in select if field != rows_from]
    if not plain:
        raise ValueError(
            f"rows_from={rows_from!r} makes one row per child, so select the columns that say whose row it is"
        )

    records: List[Dict[str, Any]] = []
    child_columns: Dict[str, None] = {}
    for item in items:
        base = {key: _value(item.properties.get(key), raw) for key in plain}
        for child in _children(item.properties.get(rows_from)):
            values = _child_values(child, raw, rows_from)
            child_columns.update(dict.fromkeys(values))
            records.append({**base, **values})
    return [
        {**{key: record.get(key) for key in plain}, **{key: record.get(key) for key in child_columns}}
        for record in records
    ]


def _children(value: Any) -> List[Any]:
    """The child values of a collection property, or one empty row when it holds none."""
    if value is None:
        return [{}]
    if isinstance(value, (list, tuple, ClientValueCollection, ClientObjectCollection)):
        return list(value) or [{}]
    return [value]


def _child_values(child: Any, raw: bool, rows_from: str) -> Dict[str, Any]:
    """A child's fields as a record: declared order, spelled as the serializer spells them.

    A schema value is read field by field rather than straight off ``to_json``, because
    the serializer drops what a *request* would leave out — an empty collection, an unset
    member — while a row needs the column to exist.
    """
    if isinstance(child, dict):
        return dict(child)
    if isinstance(child, ClientValue):
        sent = {} if raw else child.to_json()
        schema = TypeSchema.of(type(child))
        values: Dict[str, Any] = {}
        for attr, value in child:
            if attr.startswith("__"):
                continue
            name = schema.declared(attr)
            spelled = name.name if name is not None else attr
            values[spelled] = value if raw else sent.get(spelled)
        return values
    if raw:
        return dict(child.properties)
    value = serialize_value(child)
    return value if isinstance(value, dict) else {rows_from: value}


def _value(value: Any, raw: bool) -> Any:
    """Coerce a property value to its JSON-safe form unless ``raw`` is requested."""
    return value if raw else serialize_value(value)


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


def _property_value(prop: "dict | ClientObject", field_name: str, raw: bool = False) -> Any:
    """Read a property value from an item that may be a ClientObject or dict."""
    if isinstance(prop, dict):
        return _value(prop.get(field_name), raw)
    return _value(prop.properties.get(field_name), raw)
