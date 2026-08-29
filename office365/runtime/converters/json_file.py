"""JSON (array) file exporter/importer — stdlib only.

Unlike NDJSON (one JSON object per line), this writes/reads a single JSON array
of records — useful for round-tripping an export verbatim.
"""

from __future__ import annotations

import json
from typing import IO, Any, Dict, List


def write_json(records: List[Dict[str, Any]], file: IO[str]) -> None:
    """Write records as a JSON array."""
    json.dump(records, file)


def read_json(file: IO[str]) -> List[Dict[str, Any]]:
    """Read a JSON array of records."""
    data = json.load(file)
    return data if isinstance(data, list) else []
