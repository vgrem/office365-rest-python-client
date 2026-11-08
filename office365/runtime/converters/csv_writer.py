"""CSV exporter — reuses the shared record projection (``records.iter_records``)."""

from __future__ import annotations

import csv
from typing import IO, Any, Iterable, List, Optional

from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.converters.records import iter_records
from office365.runtime.converters.value import serialize_value


def _cell(value: Any) -> str:
    """Serialize a stored value and render it as a CSV cell."""
    value = serialize_value(value)
    if value is None:
        return ""
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (list, tuple)):
        return "; ".join(str(item) for item in value)
    return str(value)


def write_csv(
    collection: ClientObjectCollection, file: IO[str], delimiter: str = ",", rows_from: Optional[str] = None
) -> None:
    """Write collection items to CSV using the shared record projection.

    The projection (``records.iter_records``) asks the type for its columns: when no
    ``.select()`` is set the declared ones come first, in declaration order, and a
    name only the page carries follows. Plain select fields (e.g. ``"displayName"``)
    produce one column; dotted select fields (e.g. ``"members/displayName"``) walk
    into an expanded navigation property — one CSV row is emitted per child item.

    ``rows_from`` fans out over a collection-valued property instead — one row per
    child, the child's own properties as columns. Graph offers no projection for it:
    a complex collection cannot be ``$expand``-ed and its fields cannot be named in
    ``$select``, so the row unit has to be stated.

    Usage:
        >>> collection.get_all() \\
        ...     .select(["displayName", "members/displayName", "members/email"]) \\
        ...     .expand(["members"]) \\
        ...     .to_csv(f) \\
        ...     .execute_query()
        >>> client.users.get_licensed().select(["userPrincipalName"]).get_all() \\
        ...     .to_csv(f, rows_from="assignedLicenses") \\
        ...     .execute_query()
    """
    write_records(iter_records(collection, rows_from=rows_from), file, delimiter=delimiter)


def write_records(
    records: Iterable[dict], file: IO[str], columns: Optional[List[str]] = None, delimiter: str = ","
) -> None:
    """Write a list of dict records to CSV.

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
