"""The CSV reader: rows in, plain dict records out (the mirror of ``csv_writer``).

Format parsing only. Typing and filtering a record against a model is
:func:`~office365.runtime.converters.records.deserialize_records`, which every format shares.
"""

from __future__ import annotations

import csv
from typing import IO, TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from office365.runtime.converters.streams import Source


def csv_rows(stream: IO[str], delimiter: str = ",") -> Iterator[dict]:
    """Yield CSV rows as records, dropping empty cells (a cell states nothing)."""
    for row in csv.DictReader(stream, delimiter=delimiter):
        yield {key: value for key, value in row.items() if value not in ("", None)}


def read_csv_records(file: IO[str], delimiter: str = ",") -> list[dict]:
    """Parse CSV rows into plain dict records (empty cells dropped).

    Type-aware normalization (dotted keys, ``"; "`` collection splitting, unknown-column
    skipping) is applied by
    :func:`~office365.runtime.converters.records.deserialize_records` on import.
    """
    return list(csv_rows(file, delimiter))


def csv_batches(source: Source, chunk: int, delimiter: str = ",") -> Iterator[list[dict]]:
    """Read a CSV source as batches of records, streaming the file.

    The import path's reader: a file of any size is never held whole, only one batch.
    """
    from office365.runtime.converters.streams import open_text

    with open_text(source) as stream:
        batch: list[dict] = []
        for row in csv_rows(stream, delimiter):
            batch.append(row)
            if len(batch) >= chunk:
                yield batch
                batch = []
        if batch:
            yield batch
