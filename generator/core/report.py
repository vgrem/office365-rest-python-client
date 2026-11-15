"""Writing a plan where a reviewer can read it.

Five commands take a ``--report`` path and each used to open the file itself. One
writer keeps the indentation, the newline and the encoding the same for all of them,
so a report from ``--audit`` and one from ``--place`` diff the same way.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json(payload: Any, path: str | Path) -> Path:
    """Write ``payload`` as indented JSON, newline-terminated, and answer the path."""
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2, sort_keys=False)
        stream.write("\n")
    return Path(path)
