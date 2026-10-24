"""The adapter shapes every Outlook family shares, and the mail export on top of them.

Three families (mail, calendar, contacts) are three of the same job, so the parts that do
not differ are stated once:

* :class:`ServiceSource` — a Graph collection read once, with the handles kept beside the
  planned items, so a plan loaded from disk can still be read without a second pass;
* :class:`SidecarTreeTarget` — an export tree: one payload file plus one JSON sidecar per
  item, and an index rebuilt from the sidecars at ``commit()`` so a resumed run's manifest
  is complete.

What is left to a family is its record (:mod:`office365.migration.outlook.records`) and the
source/target that speak to its own collection. This module is where the mail ones live,
because the export tree's shape was written for mail first::

    from office365.migration import MigrationJob
    from office365.migration.outlook import MailExportOptions, MailExportTarget, MailFolderSource

    folder = client.me.mail_folders["inbox"].get().execute_query()
    job = MigrationJob(MailFolderSource(folder), MailExportTarget("./mailbox-export"))
    job.plan()
    job.run()
    print(job.verify().summary())

Export layout (the convention all three families share)::

    <root>/<folder>/<YYYY-MM-DD>_<subject-slug>_<id-digest>.eml   RFC 822 bytes
    <root>/<folder>/<same stem>.json                              sidecar record
    <root>/manifest.jsonl                                         one sidecar per line

The ``.eml`` is the portable artefact: it opens in Outlook, Thunderbird, macOS Mail, and
any IMAP server accepts it as an ``APPEND``. Everything MIME cannot carry (Graph ids, read
state, categories, conversation id) lives in the sidecar, which is also what a later import
reads to restore them.

Two honest limits: attachments ride **inside** the MIME payload (so they are not separate
manifest items), and the MIME body is fetched per message — the export does not batch those
reads (``Message.get_content`` is batchable since 3.3.0, so a reader that batches them is a
tuning step, not a redesign).
"""

from __future__ import annotations

import json
import os
from datetime import timezone
from pathlib import Path
from typing import Any, ClassVar, Dict, Generic, Iterable, List, Optional, Type, TypeVar

from office365.migration.adapters import DataSource, DataTarget, MigrationProgress, checksum
from office365.migration.base import MigrationItem
from office365.migration.outlook.fidelity import MAIL_EXPORT_DIMENSIONS
from office365.migration.outlook.models import MailExportOptions, MessageRecord
from office365.migration.outlook.records import SidecarRecord, slug
from office365.outlook.mail.folders.folder import MailFolder
from office365.outlook.mail.messages.message import Message
from office365.runtime.converters.scalars import parse_datetime
from office365.runtime.operations import emit_progress

#: The index file a target writes at ``commit()`` (one JSON record per line).
MANIFEST_NAME = "manifest.jsonl"

#: The sidecar beside each payload: the export writes ``<stem>.json`` next to ``<stem>.<suffix>``.
SIDECAR_SUFFIX = ".json"

#: The service object a source keeps beside each planned item.
_Handle = TypeVar("_Handle")

#: The record type a tree holds, so a family's source answers its own record class.
_TreeRecord = TypeVar("_TreeRecord", bound=SidecarRecord)


class ServiceSource(DataSource, Generic[_Handle]):
    """A Graph collection read once, with the handle every planned item came from.

    ``metadata`` on an item is the record (JSON), so a plan loaded from disk carries no
    service objects; the handles live here and are rebuilt by one enumeration if the plan
    outlived the process.
    """

    def __init__(self) -> None:
        self._handles: Dict[str, _Handle] = {}  # dest path -> service object
        self._enumerated = False

    def _remember(self, item: MigrationItem, handle: _Handle) -> None:
        """Keep the object a planned item was read from."""
        self._handles[item.dest_path] = handle

    def _handle(self, item: MigrationItem) -> _Handle:
        """The service object for an item, enumerating once if the plan came from disk."""
        handle = self._handles.get(item.dest_path)
        if handle is None and not self._enumerated:
            self.list_items()
            handle = self._handles.get(item.dest_path)
        if handle is None:
            raise KeyError(f"{item.dest_path!r} was not enumerated by this source — re-plan the job")
        return handle


class MailFolderSource(ServiceSource[Message]):
    """Enumerates a Graph mail folder (recursively) as one item per message.

    Each item carries its record in ``metadata``, so the export's index is written from the
    manifest itself — no second pass over the mailbox.
    """

    #: A mailbox has none of the SharePoint dimensions; see ``outlook.fidelity``.
    fidelity_dimensions = MAIL_EXPORT_DIMENSIONS

    def __init__(self, folder: MailFolder, options: MailExportOptions | None = None) -> None:
        super().__init__()
        self._folder = folder
        self._options = options or MailExportOptions()

    def label(self) -> str:
        name = self._options.root_name or getattr(self._folder, "display_name", None) or self._folder.id
        return f"mail:{name}"

    def list_items(self, progress: MigrationProgress = None) -> List[MigrationItem]:
        root = self._options.root_name or slug(getattr(self._folder, "display_name", None)) or "mailbox"
        display = getattr(self._folder, "display_name", None) or root
        items: List[MigrationItem] = []
        self._collect(self._folder, root, display, items, progress)
        self._enumerated = True
        return items

    def _collect(
        self, folder: MailFolder, path: str, display: str, items: List[MigrationItem], progress: MigrationProgress
    ) -> None:
        for message in folder.messages.select(list(MessageRecord.columns)).get_all().execute_query():
            if message.is_draft and not self._options.include_drafts:
                continue
            item = self._item(message, path, display)
            self._remember(item, message)
            items.append(item)
            emit_progress(progress, done=len(items), stage="planning", items=[item])
        if not self._options.include_subfolders:
            return
        for child in folder.child_folders.get().execute_query():
            name = slug(getattr(child, "display_name", None)) or str(child.id)
            child_display = getattr(child, "display_name", None) or name
            self._collect(child, f"{path}/{name}", f"{display}/{child_display}", items, progress)

    def _item(self, message: Message, path: str, display: str) -> MigrationItem:
        record = MessageRecord.of(message, path, display, self._options.extra_properties)
        return MigrationItem(
            source_path=record.dest_path,
            dest_path=record.dest_path,
            # The projection cannot ask for ``size`` (the backend rejects the column), so
            # the count is filled in by ``read()`` once the bytes are in hand.
            size_bytes=0,
            item_type=MessageRecord.item_type,
            modified=record.modified,
            created=record.created,
            source_id=record.source_id,
            metadata=record.to_json(),
        )

    def read(self, item: MigrationItem) -> bytes:
        """The message's RFC 822 bytes (``GET /messages/{id}/$value``)."""
        data = self._handle(item).get_content().execute_query().value
        item.size_bytes = len(data)
        return data

    def checksum(self, item: MigrationItem) -> str:
        return checksum(self.read(item))


class SidecarTreeTarget(DataTarget):
    """Writes an export tree: one payload file plus one JSON sidecar per item.

    The convention all three Outlook exports share — the payload is the portable artefact
    (MIME bytes, an ``.ics`` document, a vCard), the sidecar is the record an import
    replays, and ``commit()`` rebuilds the index from the sidecars so a resumed run's
    manifest is complete. A subclass names its :attr:`record` and nothing else.
    """

    #: The record type this tree holds: it names the payload's suffix and the sidecar key
    #: that points at it, so a family cannot add one and forget the other.
    record: ClassVar[Type[SidecarRecord]]

    @property
    def content_suffix(self) -> str:
        """The payload file's extension (``.eml``, ``.ics``, ``.vcf``)."""
        return self.record.content_suffix

    @property
    def payload_key(self) -> str:
        """The sidecar key recording where the payload was written."""
        return self.record.provenance[2]

    def __init__(self, root: str | Path, write_manifest: bool = True) -> None:
        self._root = Path(root)
        self._root.mkdir(parents=True, exist_ok=True)
        self._write_manifest = write_manifest

    @property
    def root(self) -> Path:
        return self._root

    def label(self) -> str:
        return str(self._root)

    def _path(self, item: MigrationItem) -> Path:
        return self._root / item.dest_path

    def _sidecar(self, item: MigrationItem) -> Path:
        return self._path(item).with_suffix(".json")

    def exists(self, item: MigrationItem) -> bool:
        return self._path(item).exists()

    def write(self, item: MigrationItem, payload: Any) -> None:
        path = self._path(item)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = payload if isinstance(payload, bytes) else bytes(payload)
        path.write_bytes(data)
        envelope = dict(item.metadata or {})
        envelope.setdefault(self.payload_key, item.dest_path)
        envelope.setdefault("source_id", item.source_id)
        envelope["size_bytes"] = len(data)
        self._sidecar(item).write_text(json.dumps(envelope, indent=2, default=str), encoding="utf-8")

    def list_paths(self) -> Iterable[str]:
        """Every payload file under the root (sidecars and the index are not content)."""
        pattern = f"*{self.content_suffix}"
        return (p.relative_to(self._root).as_posix() for p in sorted(self._root.rglob(pattern)))

    def checksum(self, item: MigrationItem) -> str:
        return checksum(self._path(item).read_bytes())

    def apply_timestamps(self, item: MigrationItem) -> None:
        """Stamp the payload file with the item's last-modified time (``preserve_timestamps``).

        An export tree has no per-item metadata the filesystem honours, so the file mtime
        is the only timestamp it can really preserve; the sidecar keeps the original values
        either way.
        """
        stamp = item.modified
        path = self._path(item)
        if not stamp or not path.exists():
            return
        parsed = parse_datetime(str(stamp))
        if parsed is None:
            return
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        seconds = parsed.timestamp()
        os.utime(path, (seconds, seconds))

    def read_metadata(self, item: MigrationItem) -> Optional[Dict[str, Any]]:
        """The sidecar record (what the export recorded about this item)."""
        sidecar = self._sidecar(item)
        return json.loads(sidecar.read_text(encoding="utf-8")) if sidecar.exists() else None

    def commit(self, options: Any = None) -> None:
        """Write ``manifest.jsonl`` — read back from the sidecars, so a resumed run's index is complete."""
        if not self._write_manifest:
            return
        records = []
        for sidecar in sorted(self._root.rglob("*.json")):
            records.append(json.loads(sidecar.read_text(encoding="utf-8")))
        lines = "".join(json.dumps(record, default=str) + "\n" for record in records)
        (self._root / MANIFEST_NAME).write_text(lines, encoding="utf-8")

    def close(self) -> None:
        pass


class SidecarTreeSource(DataSource, Generic[_TreeRecord]):
    """Reads an exported tree back: each payload file plus the JSON sidecar beside it.

    The mirror of :class:`SidecarTreeTarget`, and the reason the three import sources are
    one shape: a tree is a tree, and a record (:class:`SidecarRecord`) already answers
    everything an item needs — its identity, its stamps, its payload's extension and what
    a verification compares. A subclass names its :attr:`record` and the notes that say
    why its sidecar cannot be omitted.
    """

    #: The record type this tree holds; it names the payload's suffix and the item type.
    record: Type[_TreeRecord]
    #: Whether a payload without a sidecar is an error. A calendar's or a contact's is: the
    #: document cannot carry what the sidecar does (Graph's recurrence object, the office
    #: fields and address components). A mailbox's is not — the RFC 822 bytes are complete
    #: on their own, so a bare ``.eml`` tree still imports, with no flags to replay.
    sidecar_required: ClassVar[bool] = True
    #: Why this family's sidecar is required, in one sentence, appended to the error.
    sidecar_note: ClassVar[str] = ""

    def __init__(self, root: str | Path, options: Any = None) -> None:
        self._root = Path(root)
        self._options = options or self.record.options_class()

    @property
    def root(self) -> Path:
        return self._root

    def label(self) -> str:
        return f"{self.record.content_suffix.lstrip('.')}:{self._root}"

    def list_items(self, progress: MigrationProgress = None) -> List[MigrationItem]:
        if not self._root.is_dir():
            raise FileNotFoundError(f"{self._root} is not a directory of exported {self.record.content_suffix} files")
        items: List[MigrationItem] = []
        for path in sorted(self._root.rglob(f"*{self.record.content_suffix}")):
            item = self._item(path)
            items.append(item)
            emit_progress(progress, done=len(items), stage="planning", items=[item])
        return items

    def _item(self, path: Path) -> MigrationItem:
        dest = path.relative_to(self._root).as_posix()
        envelope = self._sidecar(path)
        record = self.record.from_json(envelope)
        return MigrationItem(
            source_path=dest,
            dest_path=dest,
            size_bytes=path.stat().st_size,
            item_type=self.record.item_type,
            modified=record.modified,
            created=record.created,
            source_id=record.source_id,
            metadata=envelope or None,
        )

    def _sidecar(self, path: Path) -> Dict[str, Any]:
        """The sidecar beside a payload file, or an empty envelope when the family allows none."""
        sidecar = path.with_suffix(SIDECAR_SUFFIX)
        if not sidecar.exists():
            if self.sidecar_required:
                raise FileNotFoundError(f"{sidecar} is missing: {self.sidecar_note}")
            return {}
        return json.loads(sidecar.read_text(encoding="utf-8"))

    def _path(self, item: MigrationItem) -> Path:
        path = self._root / item.dest_path
        if self._root.resolve() not in path.resolve().parents:
            raise ValueError(f"{item.dest_path!r} escapes the export tree")
        return path

    def _record(self, item: MigrationItem) -> _TreeRecord:
        """The record a planned item's sidecar holds."""
        return self.record.from_json(self._sidecar(self._path(item)))

    def read(self, item: MigrationItem) -> bytes:
        """The payload file's bytes."""
        return self._path(item).read_bytes()

    def checksum(self, item: MigrationItem) -> str:
        """What a verification compares for this item — the record's own rule, not the bytes.

        A family whose document this package renders (``.ics``, ``.vcf``) is checkable by
        them; one whose artefact the service re-serializes (``.eml``) is not, and its
        record answers a digest of what the message says instead. The caller only asks.
        """
        return self._record(item).checksum(self.read(item), self._options)


class MailExportTarget(SidecarTreeTarget):
    """Writes a portable EML tree: one ``.eml`` plus one JSON sidecar per message."""

    fidelity_dimensions = MAIL_EXPORT_DIMENSIONS
    record = MessageRecord


__all__ = [
    "MANIFEST_NAME",
    "SIDECAR_SUFFIX",
    "MailExportTarget",
    "MailFolderSource",
    "ServiceSource",
    "SidecarTreeSource",
    "SidecarTreeTarget",
]
