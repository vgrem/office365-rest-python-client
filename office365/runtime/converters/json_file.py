"""JSON (array) file exporter/importer — stdlib only.

Unlike NDJSON (one JSON object per line), this writes/reads a single JSON array
of records — useful for round-tripping an export verbatim.
"""

from __future__ import annotations

import json
from typing import IO, Any, Dict, List, Optional


def write_json(records: List[Dict[str, Any]], file: IO[str], indent: Optional[int] = None) -> None:
    """Write records as a JSON array."""
    json.dump(records, file, indent=indent, default=str)


def read_json(file: IO[str]) -> List[Dict[str, Any]]:
    """Read a JSON array of records."""
    data = json.load(file)
    return data if isinstance(data, list) else []


def record_to_json(payload: Any) -> str:
    """Serialize a record to the canonical JSON text used when persisting it.

    Non-JSON values (entity/datetime objects) fall back to ``str`` so the text is
    stable — source and target checksums both use this form.
    """
    return json.dumps(payload, indent=2, default=str)
