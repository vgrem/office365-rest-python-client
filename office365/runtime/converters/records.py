"""The plain dict records both directions speak.

Export: ``iter_records`` turns a loaded collection into records, and every tabular
writer consumes that. Import: ``deserialize_records`` turns a source -- a path, a
stream, a DataFrame, or rows already read -- into the payload of a create/update.
Both answer with the type's names, not the page's or the file's: a row should carry the
same names the serializer, ``$select`` and the migration imports use, or every format
re-derives them for itself.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, Dict, List, cast, get_origin

from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.converters.csv_writer import LIST_SEPARATOR
from office365.runtime.converters.named import Converter, ConverterSpec, converter_for
from office365.runtime.converters.registry import reader_for
from office365.runtime.converters.value import declared_type, serialize_value
from office365.runtime.schema import TypeSchema
from office365.runtime.types.odata_property import request_version

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject
    from office365.runtime.converters.streams import Source


def iter_records(
    collection: "ClientObjectCollection", raw: bool = False, rows_from: str | None = None
) -> List[Dict[str, Any]]:
    """Project a loaded collection into plain dict records.

    Feeds ``csv_writer.write_records``: plain select fields become columns,
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
        columns = TypeSchema.of(type(child)).columns
        if raw:
            return {name: child.get_property(name) for name in columns}
        sent = child.to_json()
        return {name: sent.get(name) for name in columns}
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


def deserialize_records(
    item_type: type,
    records: "list[dict] | Source",
    *,
    format: "str | None" = None,  # noqa: A002
    converters: "dict[str, ConverterSpec] | None" = None,
    allow_unknown: bool = False,
) -> list[dict]:
    """Normalize plain dict records to the entity's declared property types.

    ``format`` names the reader that turns a *source* -- a path, a URL, a stream, a
    DataFrame -- into records, so a caller with no collection to hand a source to reads
    with one call: ``deserialize_records(T, path, format="csv")``. Without it, ``records``
    is already records.

    Dotted keys (``a/b/c``) are re-nested into dicts; ``"; "``-joined strings are
    split for collection-typed fields; non-importable keys (``@*``, ``id``) and
    ``None`` cells are dropped; columns mapping to no known property are skipped
    with a warning. Pass ``allow_unknown=True`` for schema-flexible targets whose
    fields are only known at runtime (SharePoint list items). Shared by every
    import format.

    ``converters`` maps a *record key* (dotted keys included) to one value converter, as a
    callable, a Python type, a type name or a ``FieldType`` -- see
    :func:`~office365.runtime.converters.named.converter_for`. A converter wins over
    the column's declared type; a converter naming a column the type does not declare
    raises, so a typo cannot silently drop the column it meant to type.
    """
    if format is not None:
        records = reader_for(format)(records)
    resolved = resolve_converters(item_type, converters, allow_unknown)
    warn = warnings.warn

    def split_members(raw: Any) -> Any:
        # A member is never empty: ``"p1; p2"`` is two plans, ``"; p1"`` is one.
        if not isinstance(raw, str):
            return raw
        return [part for part in raw.split(LIST_SEPARATOR) if part]

    def plan_for(key: str) -> tuple:
        """How a column's cells are stored: (importable, unknown, path, leaf, convert).

        Every row of an import shares its columns, so this -- the importable check, the
        declared-type lookup, the dotted-key split and the collection check -- runs once
        per column instead of once per cell.
        """
        if not _is_importable(key):
            return False, False, None, key, None
        convert = resolved.get(key)
        *path, leaf = key.split("/")
        declared = declared_type(item_type, path[0] if path else leaf)
        if declared is None:
            return True, not allow_unknown, path or None, leaf, convert
        if not path and convert is None and _is_collection(declared):
            convert = split_members
        return True, False, path or None, leaf, convert

    plans: dict[str, tuple] = {}
    deserialized: list[dict[str, Any]] = []
    append = deserialized.append
    for record in cast("list[dict]", records):
        item: dict[str, Any] = {}
        for key, raw in record.items():
            if raw is None:
                continue
            try:
                importable, unknown, path, leaf, convert = plans[key]
            except KeyError:
                importable, unknown, path, leaf, convert = plans[key] = plan_for(key)
            if not importable:
                continue
            if unknown:
                warn(f"Skipping unknown column '{key}'", stacklevel=2)
                continue
            value = raw if convert is None else convert(raw)
            if path is None:
                item[leaf] = value
            else:
                _set_nested(item, path, leaf, value)
        append(item)
    return deserialized


def apply_converters(records: list[dict], converters: dict[str, "Converter"]) -> list[dict]:
    """Apply resolved converters cell by cell, leaving every other key untouched.

    No filtering and no declared-type work: this is the user's ``converters`` layer alone,
    so it can run before a keyed import where the key columns need not be declared on
    the model. ``None`` cells are skipped (an empty cell states nothing).
    """
    if not converters:
        return records
    return [
        {
            key: (converters[key](value) if key in converters and value is not None else value)
            for key, value in record.items()
        }
        for record in records
    ]


def resolve_converters(
    item_type: type,
    converters: "dict[str, ConverterSpec] | None",
    allow_unknown: bool,
) -> dict[str, "Converter"]:
    """Resolve every per-column spec once, and reject keys the type cannot store."""
    if not converters:
        return {}
    resolved: dict[str, Converter] = {}
    for column, spec in converters.items():
        if declared_type(item_type, column.split("/", 1)[0]) is None and not allow_unknown:
            raise ValueError(
                f"converters has no column {column!r} in {item_type.__name__}; "
                "check the destination key, or pass allow_unknown=True for a target that accepts arbitrary columns"
            )
        resolved[column] = converter_for(spec)
    return resolved


def _is_importable(key: str) -> bool:
    """Decide whether a record key should be imported at all."""
    return not key.startswith("@") and key != "id"


def _is_collection(target_type: Any) -> bool:
    """Decide whether a declared type represents a list/collection field."""
    return get_origin(target_type) in (list, tuple, set) or (
        isinstance(target_type, type) and issubclass(target_type, ClientValueCollection)
    )


def _set_nested(record: dict[str, Any], path: list[str], leaf: str, value: Any) -> None:
    """Re-nest a dotted header (``a/b/c``, pre-split into its path and leaf) into nested dicts."""
    node = record
    for part in path:
        node = node.setdefault(part, {})
    node[leaf] = value
