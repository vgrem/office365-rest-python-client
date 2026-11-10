"""The CSV sink: records in, a file out (the mirror of ``csv_reader``)."""

from __future__ import annotations

import csv
from typing import IO, Any, Iterable, List, Optional

from office365.runtime.converters.value import serialize_value

#: How a list is spelled in one cell; the reader splits at the same separator.
LIST_SEPARATOR = "; "


def _cell(value: Any) -> str:
    """Serialize a stored value and render it as a CSV cell."""
    value = serialize_value(value)
    if value is None:
        return ""
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (list, tuple)):
        return LIST_SEPARATOR.join(str(item) for item in value)
    return str(value)


def write_records(
    records: Iterable[dict], file: IO[str], columns: Optional[List[str]] = None, delimiter: str = ","
) -> None:
    """Write records to CSV — the sink of the record flow, shared by every exporter.

    The records come from the type, not from the response: ``iter_records`` asks the
    model for its columns, so when no ``.select()`` is set the declared ones come
    first, in declaration order, and a name only the page carries follows. Plain
    select fields (e.g. ``"displayName"``) produce one column; dotted select fields
    (e.g. ``"members/displayName"``) walk into an expanded navigation property — one
    row is emitted per child item. ``rows_from`` fans out over a collection-valued
    property instead, one row per child with the child's own properties as columns:
    Graph offers no projection for that (a complex collection cannot be ``$expand``-ed
    and its fields cannot be named in ``$select``), so the row unit is stated.

    Usage:
        >>> collection.get_all() \
        ...     .select(["displayName", "members/displayName", "members/email"]) \
        ...     .expand(["members"]) \
        ...     .to_csv(f) \
        ...     .execute_query()
        >>> client.users.get_licensed().select(["userPrincipalName"]).get_all() \
        ...     .to_csv(f, rows_from="assignedLicenses") \
        ...     .execute_query()

    Args:
        records: Rows as dicts (one dict per line), or any iterable of them — a
            generator that walks the tenant is materialized here so the column
            order can be read off the rows.
        file: Writable text stream.
        columns: Explicit column order; defaults to the union of record keys
            in first-appearance order.
    """
    records = list(records)
    if not records:
        return
    if columns is None:
        columns = list(dict.fromkeys(key for record in records for key in record))
    writer = csv.writer(file, delimiter=delimiter)
    writer.writerow(columns)
    write_rows(records, file, columns, delimiter)


def write_rows(records: list[dict], file: IO[str], columns: list[str], delimiter: str = ",") -> None:
    """Write data rows only (no header) — used by the paged/streaming exporter."""
    writer = csv.writer(file, delimiter=delimiter)
    for record in records:
        writer.writerow([_cell(record.get(key)) for key in columns])
