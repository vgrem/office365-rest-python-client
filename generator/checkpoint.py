"""Resumable run state: which types have already been processed."""

from __future__ import annotations

import json
from pathlib import Path


def checkpoint_path(metadata_path: str, base_dir: Path) -> Path:
    """The checkpoint file for a metadata source (``.checkpoints/<name>.json``)."""
    return base_dir / ".checkpoints" / f"{Path(metadata_path).name}.json"


class Checkpoint:
    """Tracks processed types so an interrupted run can resume.

    Not persisted in dry-run mode, so a dry-run never alters resume state.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self.processed: set[str] = set()
        if path.exists():
            self.processed = set(json.loads(path.read_text(encoding="utf-8")))
            print(f"Resuming from checkpoint: {len(self.processed)} types already processed")

    def add(self, name: str, *, persist: bool = True) -> None:
        self.processed.add(name)
        if persist:
            self.save()

    def save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(sorted(self.processed)), encoding="utf-8")

    def clear(self) -> None:
        if self._path.exists():
            self._path.unlink()
