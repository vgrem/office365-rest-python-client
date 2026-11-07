"""A portable bundle: one directory that *is* the export.

A filesystem export is a copy of the content plus whatever the caller remembers
about it — the tree says which files were moved, and a sidecar placed beside it
says what they were. That works because the caller is still there to name the
sidecar. A bundle has to answer for itself: every payload is stored once, under
the SHA-256 of its content, and one append-only ledger names each item, so the
export can be deduplicated, resumed, hashed as a whole, and read back into any
target without the source.

Layout::

    bundle/
      bundle.json                     # written at commit: counts, bytes, one rollup
      manifest.ndjson                 # one ledger row per item, appended as it lands
      content/<sha256[:2]>/<sha256>   # the payload, once, however many items point at it

A folder is a ledger row with no payload: an empty folder is part of what was
migrated, and nothing else in this layout could say that it existed.

:class:`BundleTarget` writes that directory and :class:`BundleSource` reads it
back, so an export and an import are two jobs over the same artefact.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from office365.migration.adapters import MigrationProgress, checksum_file
from office365.migration.base import MigrationItem
from office365.runtime.converters.json_file import record_to_json
from office365.runtime.converters.scalars import utc_now_iso
from office365.runtime.operations import emit_progress
from office365.runtime.persistence import atomic_write_json

#: On-disk format of the bundle itself, so a later reader can refuse one it does
#: not understand instead of misreading it.
BUNDLE_FORMAT = 1
CONTENT_DIR = "content"
LEDGER_NAME = "manifest.ndjson"
INDEX_NAME = "bundle.json"


class _Bundle:
    """The bundle directory as it stands: its ledger rows and its payloads.

    Both directions read the same format, so the file names and the ledger are
    known in one place: a target asks whether a destination is already here, a
    source asks what *here* is. Only the answers that depend on the shape of the
    payload live in the two adapters.
    """

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)
        self._rows: dict[str, dict[str, Any]] = {}
        self._created_at: str | None = None
        self._load()

    @property
    def root(self) -> Path:
        return self._root

    def row(self, dest_path: str) -> dict[str, Any] | None:
        """What the bundle records about a destination (``None`` if it has no row)."""
        return self._rows.get(dest_path)

    def payload(self, dest_path: str) -> object:
        """The payload stored for a destination: bytes for content, dict for a record."""
        row = self._rows.get(dest_path)
        if row is None:
            raise FileNotFoundError(f"{dest_path!r} is not in the bundle")
        digest = row.get("sha256")
        if not digest:
            raise IsADirectoryError(f"{dest_path!r} is a folder entry: it carries no payload")
        data = self._blob_path(digest).read_bytes()
        return json.loads(data) if row.get("encoding") == "json" else data

    def checksum(self, item: MigrationItem) -> str:
        """The digest of the stored bytes, or nothing when they are not the content.

        A payload stored as JSON is a *record*: whether two records are the same
        item is the record target's question — the SharePoint adapters answer it
        over the content columns and ignore what the service assigns. Reporting the
        digest of the JSON instead would turn that comparison into a false
        mismatch, so the bundle says it cannot compare rather than answering the
        wrong thing.
        """
        row = self._rows.get(item.dest_path)
        if not row or row.get("encoding") != "bytes":
            return ""
        return checksum_file(self._blob_path(row["sha256"]))

    def modified(self, item: MigrationItem) -> str:
        """Source last-modified carried by the ledger, for an incremental re-run."""
        return (self._rows.get(item.dest_path) or {}).get("modified") or ""

    # ── Internals ────────────────────────────────────────────────

    def _load(self) -> None:
        """Re-enter an existing bundle: its index (if sealed) and its ledger.

        A later row for the same destination wins, because that is what the last
        run wrote — a ledger is a history, the bundle is its current state.
        """
        index = self._root / INDEX_NAME
        if index.exists():
            with open(index, "r", encoding="utf-8") as f:
                self._created_at = json.load(f).get("created_at")
        ledger = self._root / LEDGER_NAME
        if not ledger.exists():
            return
        with open(ledger, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    self._rows[row["dest_path"]] = row

    def _record(self, item: MigrationItem, digest: str | None, size: int, encoding: str | None) -> None:
        """Append the item's ledger row, unless the bundle already holds it.

        The row is flushed as it is written, so a crashed run leaves every payload
        it finished accounted for; ``commit`` is what makes the whole file durable.
        """
        known = self._rows.get(item.dest_path)
        if known is not None and known.get("sha256") == digest and known.get("size_bytes") == size:
            return
        row = {
            "dest_path": item.dest_path,
            "source_path": item.source_path,
            "item_type": item.item_type,
            "sha256": digest,
            "encoding": encoding,
            "size_bytes": size,
            "created": item.created,
            "modified": item.modified,
            "source_id": item.source_id,
            "metadata": item.metadata,
        }
        self._rows[item.dest_path] = row
        self._root.mkdir(parents=True, exist_ok=True)
        with open(self._root / LEDGER_NAME, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")
            f.flush()

    def _put_blob(self, digest: str, data: bytes) -> None:
        """Store the payload under its digest, atomically and only once."""
        path = self._blob_path(digest)
        if path.exists():
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=".blob.", suffix=".tmp")
        tmp = Path(tmp_name)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise

    def _blob_path(self, digest: str) -> Path:
        return self._root / CONTENT_DIR / digest[:2] / digest


class BundleTarget(_Bundle):
    """Writes a migration into a content-addressed bundle directory.

    Idempotent by construction: a payload is stored under the digest of its
    bytes, so writing the same content twice costs nothing, and a ledger row is
    only appended when a destination's content actually changes. A resumed run
    therefore continues from the ledger it already has — ``exists`` answers from
    it, and a destination whose blob is missing (a half-deleted bundle) is
    reported as absent rather than silently skipped.
    """

    def label(self) -> str:
        return f"bundle:{self._root}"

    def exists(self, item: MigrationItem) -> bool:
        """Whether the destination is in the bundle, with its payload present."""
        row = self._rows.get(item.dest_path)
        if row is None:
            return False
        digest = row.get("sha256")
        return not digest or self._blob_path(digest).exists()

    def write(self, item: MigrationItem, payload: object) -> None:
        if item.item_type == "folder":
            self._record(item, None, 0, None)
            return
        data, encoding = _payload_bytes(payload)
        digest = hashlib.sha256(data).hexdigest()
        self._put_blob(digest, data)
        self._record(item, digest, len(data), encoding)

    def list_paths(self) -> list[str]:
        """Every destination path in the ledger (folders keep their trailing slash)."""
        return list(self._rows)

    def commit(self, options=None) -> None:
        """Seal the bundle: flush the ledger and write the index over it.

        The index is derived from the ledger, never maintained separately: a
        crash mid-run leaves a ledger that the next commit summarises, and a
        resumed run re-derives the same counts from the rows it already has.
        """
        ledger = self._root / LEDGER_NAME
        if ledger.exists():
            with open(ledger, "ab") as f:
                os.fsync(f.fileno())
        blobs = {row["sha256"] for row in self._rows.values() if row.get("sha256")}
        by_type: dict[str, int] = {}
        for row in self._rows.values():
            by_type[row["item_type"]] = by_type.get(row["item_type"], 0) + 1
        # Pinned once, so re-sealing a bundle it did not change rewrites the same bytes.
        self._created_at = self._created_at or utc_now_iso()
        atomic_write_json(
            self._root / INDEX_NAME,
            {
                "format": BUNDLE_FORMAT,
                "created_at": self._created_at,
                "items": len(self._rows),
                "by_type": dict(sorted(by_type.items())),
                "bytes": sum(row.get("size_bytes") or 0 for row in self._rows.values()),
                "blobs": len(blobs),
                "rollup": _rollup(self._rows.values()),
            },
        )

    def close(self) -> None:
        pass


class BundleSource(_Bundle):
    """Reads a bundle back as a source, so an export can be imported elsewhere.

    The items it lists are the ones the export recorded — same destinations, same
    types, same last-modified — which is what makes an import resumable and
    comparable. Fidelity the bundle does not carry is simply absent: it exposes no
    ``read_permissions``/``read_version_history``, so a job asked to preserve what
    was never written refuses at ``plan()`` instead of importing nothing quietly.
    """

    def label(self) -> str:
        return f"bundle:{self._root}"

    def list_items(self, progress: MigrationProgress = None) -> list[MigrationItem]:
        items: list[MigrationItem] = []
        for row in self._rows.values():
            item = MigrationItem(
                # Where it came from, kept as provenance: the import's manifest then
                # says what this copy is a copy *of*.
                source_path=row["source_path"] or row["dest_path"],
                dest_path=row["dest_path"],
                size_bytes=row.get("size_bytes") or 0,
                item_type=row["item_type"],
                modified=row.get("modified"),
                created=row.get("created"),
                source_id=row.get("source_id"),
                metadata=row.get("metadata"),
            )
            items.append(item)
            emit_progress(progress, done=len(items), stage="planning", items=[item])
        return items

    def read(self, item: MigrationItem) -> object:
        return self.payload(item.dest_path)

    def close(self) -> None:
        pass


def _payload_bytes(payload: object) -> tuple[bytes, str]:
    """The payload as stored bytes, and how it was stored.

    ``bytes`` is the content itself — the digest of the file is the digest of what
    the bundle holds. ``json`` is a record, whose bytes are a *serialization* of a
    value the target decides how to compare.
    """
    if isinstance(payload, bytes):
        return payload, "bytes"
    if isinstance(payload, bytearray):
        return bytes(payload), "bytes"
    if isinstance(payload, (dict, list)):
        return record_to_json(payload).encode("utf-8"), "json"
    return str(payload).encode("utf-8"), "text"


def _rollup(rows) -> str:
    """One digest over every destination and its content, so a bundle can be compared.

    Order-independent (the rows are sorted), and a folder contributes only its
    path: it has no payload of its own.
    """
    digest = hashlib.sha256()
    for row in sorted(rows, key=lambda r: r["dest_path"]):
        digest.update(f"{row['dest_path']}\0{row.get('sha256') or ''}\n".encode("utf-8"))
    return digest.hexdigest()


__all__ = ["BundleSource", "BundleTarget", "BUNDLE_FORMAT", "CONTENT_DIR", "LEDGER_NAME", "INDEX_NAME"]
