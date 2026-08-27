"""CSV exporter — reuses the shared record projection (``records.iter_records``)."""

from __future__ import annotations

import csv
from typing import IO, Any, List, Optional

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


def write_csv(collection: ClientObjectCollection, file: IO[str]) -> None:
    """Write collection items to CSV using the shared record projection.

    The projection (``records.iter_records``) mirrors the previous behaviour:
    when no ``.select()`` is set all item properties are exported; plain select
    fields (e.g. ``"displayName"``) produce one column; dotted select fields
    (e.g. ``"members/displayName"``) walk into an expanded navigation property —
    one CSV row is emitted per child item.

    Usage:
        >>> collection.get_all() \\
        ...     .select(["displayName", "members/displayName", "members/email"]) \\
        ...     .expand(["members"]) \\
        ...     .to_csv(f) \\
        ...     .execute_query()
    """
    write_records(iter_records(collection), file)


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
        writer.writerow([_cell(record.get(key)) for key in columns])
