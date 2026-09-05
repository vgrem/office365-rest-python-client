"""Filesystem source/target adapters.

A pure-stdlib adapter pair that copies a directory tree — the reference
implementation and the primary storage for the migration toolkit — plus a
:class:`JsonFileTarget` for persisting record payloads (one JSON file per item).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from office365.migration._util import emit_progress, iso
from office365.migration.adapters import MigrationProgress
from office365.migration.base import MigrationItem


class FileSystemSource:
    """Enumerates and reads files under a root directory."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)

    @property
    def root(self) -> Path:
        return self._root

    def label(self) -> str:
        return str(self._root)

    def list_items(self, progress: MigrationProgress = None) -> list[MigrationItem]:
        items: list[MigrationItem] = []
        for path in sorted(self._root.rglob("*")):
            if not path.is_file():
                continue
            stat = path.stat()
            item = MigrationItem(
                source_path=str(path),
                dest_path=str(path.relative_to(self._root)).replace("\\", "/"),
                size_bytes=stat.st_size,
                modified=iso(datetime.fromtimestamp(stat.st_mtime, timezone.utc)),
            )
            items.append(item)
            emit_progress(progress, done=len(items), stage="planning", items=[item])
        return items

    def read(self, item: MigrationItem) -> bytes:
        return Path(item.source_path).read_bytes()

    def checksum(self, item: MigrationItem) -> str:
        return _md5(Path(item.source_path))

    def close(self) -> None:
        pass


class FileSystemTarget:
    """Writes files under a root directory."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)

    @property
    def root(self) -> Path:
        return self._root

    def label(self) -> str:
        return str(self._root)

    def exists(self, item: MigrationItem) -> bool:
        return (self._root / item.dest_path).exists()

    def write(self, item: MigrationItem, payload: object) -> None:
        dest = self._root / item.dest_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload if isinstance(payload, bytes) else str(payload).encode("utf-8"))

    def list_paths(self) -> list[str]:
        return [str(p.relative_to(self._root)).replace("\\", "/") for p in self._root.rglob("*") if p.is_file()]

    def modified(self, item: MigrationItem) -> str:
        """Last-modified of the target file, for incremental migration."""
        return iso(datetime.fromtimestamp((self._root / item.dest_path).stat().st_mtime, timezone.utc))

    def checksum(self, item: MigrationItem) -> str:
        return _md5(self._root / item.dest_path)

    def commit(self, options=None) -> None:
        pass

    def close(self) -> None:
        pass


class JsonFileSource:
    """Reads record payloads (one JSON file per item) — the import counterpart
    of :class:`JsonFileTarget`. Enables records round-trips through the filesystem.
    """

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)

    def label(self) -> str:
        return str(self._root)

    def list_items(self, progress: MigrationProgress = None) -> list[MigrationItem]:
        items: list[MigrationItem] = []
        for path in sorted(self._root.rglob("*.json")):
            item = MigrationItem(
                source_path=str(path),
                dest_path=path.relative_to(self._root).with_suffix("").as_posix(),
                item_type="record",
            )
            items.append(item)
            emit_progress(progress, done=len(items), stage="planning", items=[item])
        return items

    def read(self, item: MigrationItem) -> object:
        with open(item.source_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def checksum(self, item: MigrationItem) -> str:
        return _md5(Path(item.source_path))

    def close(self) -> None:
        pass


class JsonFileTarget(FileSystemTarget):
    """Persists record payloads (dicts) as one JSON file per item.

    An interchange format for migrating tabular data (SharePoint lists,
    PostgreSQL tables, ...) through the filesystem — a stepping stone for
    S3/object-storage targets.
    """

    def _path(self, item: MigrationItem) -> Path:
        return self._root / f"{item.dest_path}.json"

    def exists(self, item: MigrationItem) -> bool:
        return self._path(item).exists()

    def write(self, item: MigrationItem, payload: object) -> None:
        dest = self._path(item)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    def list_paths(self) -> list[str]:
        return [p.relative_to(self._root).with_suffix("").as_posix() for p in self._root.rglob("*.json")]

    def checksum(self, item: MigrationItem) -> str:
        return _md5(self._path(item))


def _md5(path: Path) -> str:
    digest = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
