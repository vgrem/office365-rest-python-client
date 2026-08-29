"""NDJSON (JSON Lines) exporter/importer — stdlib only."""

from __future__ import annotations

import json
from typing import IO, Any, Dict, List


def write_ndjson(records: List[Dict[str, Any]], file: IO[str]) -> None:
    """Write records as one JSON object per line."""
    for record in records:
        file.write(json.dumps(record) + "\n")


def read_ndjson(file: IO[str]) -> List[Dict[str, Any]]:
    """Parse one JSON object per line into records."""
    return [json.loads(line) for line in file if line.strip()]
