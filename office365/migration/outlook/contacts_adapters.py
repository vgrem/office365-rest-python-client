"""Contact adapters — a Graph contact folder as a source, a vCard tree as a target, and back.

Export a contact folder::

    from office365.migration import MigrationJob
    from office365.migration.outlook import ContactExportOptions, ContactSource, VcfExportTarget

    folder = client.me.contact_folders.get().execute_query()[0]
    job = MigrationJob(ContactSource(folder), VcfExportTarget("./contacts-export"))
    job.plan()
    job.run()
    print(job.verify().summary())

Import it into another contact folder::

    from office365.migration.outlook import ContactImportOptions, ContactTarget, VcfTreeSource

    options = ContactImportOptions()
    folder = client.me.contact_folders.add("Imported").execute_query()
    job = MigrationJob(VcfTreeSource("./contacts-export", options), ContactTarget(folder, options))
    job.plan()
    job.run()
    print(job.verify().summary())

Pass the *same* options object to both sides of an import: the source computes the
content digest of what the target promises to restore.

Export layout (the same convention the mail and calendar exports use)::

    <root>/<folder>/<name-slug>_<id-digest>.vcf   vCard 3.0 document
    <root>/<folder>/<same stem>.json             sidecar record
    <root>/manifest.jsonl                        one sidecar per line

Four honest limits, all measured against Exchange:

* **A photo is not exported.** The ``contact`` entity exposes no ``hasPhoto`` column
  on this endpoint, so finding out costs one ``GET /photo`` that 404s
  (``ErrorItemNotFound``) per contact without one; on a folder of thousands that is
  a request per contact for the minority that have an image. Declared, not silent.
* **Timestamps are not restorable.** Exchange stamps a created contact with the
  import time and offers no field to set otherwise, so ``created``/``modified`` live
  in the sidecar as a record and nowhere else.
* **A birthday is normalised to a fixed time of day** (``11:59``), so an import is
  verified by the *date* it falls on rather than the instant — which is all a
  birthday ever meant.
* **A contact has no ``transactionId``**, unlike a message, so concurrency is handled
  by the target's own index (display name plus first address) instead of by the
  service refusing a second write. Two runs that overlap can therefore still import
  the same contact twice.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from office365.migration.adapters import DataTarget, MigrationProgress, checksum
from office365.migration.base import MigrationItem
from office365.migration.outlook.adapters import ServiceSource, SidecarTreeSource, SidecarTreeTarget
from office365.migration.outlook.contacts_models import (
    ContactExportOptions,
    ContactImportOptions,
    ContactRecord,
)
from office365.migration.outlook.fidelity import CONTACTS_EXPORT_DIMENSIONS, CONTACTS_IMPORT_DIMENSIONS
from office365.migration.outlook.records import slug
from office365.migration.outlook.restore import withheld
from office365.outlook.contacts.contact import Contact
from office365.outlook.contacts.folders.folder import ContactFolder
from office365.runtime.operations import emit_progress
from office365.runtime.queries.create_entity import CreateEntityQuery

#: The properties an import reads back to recognise a contact it already created.
#: Identity and the two fields a dedupe checks; narrower than ``CONTACT_COLUMNS``
#: on purpose — it runs per item. Spelled through the model so a rename cannot
#: leave it stale.
_EXISTING_COLUMNS = [Contact.odata_name(attr) for attr in ("id", "display_name", "email_addresses")]


class ContactSource(ServiceSource[Contact]):
    """Enumerates a Graph contact folder (and its children) as one item per contact.

    Each item carries its sidecar record in ``metadata``, so the export's index is
    written from the manifest itself — no second pass over the folder.
    """

    #: What a contact export preserves; see ``outlook.fidelity``.
    fidelity_dimensions = CONTACTS_EXPORT_DIMENSIONS

    def __init__(self, folder: ContactFolder, options: ContactExportOptions | None = None) -> None:
        super().__init__()
        self._folder = folder
        self._options = options or ContactExportOptions()

    def label(self) -> str:
        name = getattr(self._folder, "display_name", None) or getattr(self._folder, "id", "contacts")
        return f"contacts:{name}"

    def list_items(self, progress: MigrationProgress = None) -> list[MigrationItem]:
        path = self._options.root_name or slug(getattr(self._folder, "display_name", None)) or "contacts"
        display = getattr(self._folder, "display_name", None) or path
        items: list[MigrationItem] = []
        self._collect(self._folder, path, display, items, progress)
        self._enumerated = True
        return items

    def _collect(
        self, folder: ContactFolder, path: str, display: str, items: list[MigrationItem], progress: MigrationProgress
    ) -> None:
        for contact in folder.contacts.select(list(ContactRecord.columns)).get_all().execute_query():
            item = self._item(contact, path, display)
            self._remember(item, contact)
            items.append(item)
            emit_progress(progress, done=len(items), stage="planning", items=[item])
        if not self._options.include_subfolders:
            return
        for child in folder.child_folders.get().execute_query():
            name = slug(getattr(child, "display_name", None)) or str(child.id)
            child_display = getattr(child, "display_name", None) or name
            self._collect(child, f"{path}/{name}", f"{display}/{child_display}", items, progress)

    def _item(self, contact: Contact, path: str, display: str) -> MigrationItem:
        record = ContactRecord.of(contact, path, extra_properties=self._options.extra_properties, display_path=display)
        return MigrationItem(
            source_path=record.dest_path,
            dest_path=record.dest_path,
            # A contact has no byte size until its ``.vcf`` is rendered; ``read()`` fills it.
            size_bytes=0,
            item_type=ContactRecord.item_type,
            modified=record.modified,
            created=record.created,
            source_id=record.source_id,
            metadata=record.to_json(),
        )

    def read(self, item: MigrationItem) -> bytes:
        """The contact's vCard document, rendered from the record in ``metadata``."""
        data = ContactRecord.from_json(item.metadata or {}).vcard()
        item.size_bytes = len(data)
        return data

    def checksum(self, item: MigrationItem) -> str:
        """The ``.vcf`` bytes — this export renders them itself, so equality is fair."""
        return checksum(self.read(item))


class VcfExportTarget(SidecarTreeTarget):
    """Writes a portable vCard tree: one ``.vcf`` plus one JSON sidecar per contact."""

    fidelity_dimensions = CONTACTS_EXPORT_DIMENSIONS
    record = ContactRecord


class VcfTreeSource(SidecarTreeSource[ContactRecord]):
    """Reads an exported contact tree back as migration items.

    The ``.vcf`` is the payload (what another client opens); the JSON sidecar is the record
    the import replays, and it is **required** — a vCard cannot carry the office fields, the
    address components or the categories without a lossy mapping, and reading a contact back
    out of one would invent an import nobody verified.
    """

    #: What a contact import preserves; see ``outlook.fidelity``.
    fidelity_dimensions = CONTACTS_IMPORT_DIMENSIONS
    record = ContactRecord
    sidecar_note = (
        "the sidecar is the import contract (a vCard cannot carry the office fields, address components and"
        " categories without loss), so the tree has to come from a contact export"
    )


class ContactTarget(DataTarget):
    """Recreates exported contacts in a Graph contact folder.

    The source of truth is the sidecar, not the ``.vcf``: the create body is posted
    verbatim (:meth:`ContactRecord.payload`) because ``ContactCollection.add()``
    builds its own body from four arguments and drops everything else.
    """

    fidelity_dimensions = CONTACTS_IMPORT_DIMENSIONS

    def __init__(self, folder: ContactFolder, options: ContactImportOptions | None = None) -> None:
        self._root = folder
        self._options = options or ContactImportOptions()
        self._folders: dict[str, ContactFolder] = {}  # source directory path -> Graph folder
        self._indexed: dict[str, dict[tuple[str, str], list[Contact]]] = {}  # folder id -> dedupe index
        self._claimed: dict[tuple[str, str], int] = {}
        self._present: dict[str, Contact] = {}  # dest path -> created/found contact
        self._categories_dropped = 0
        #: Warnings a caller collects (the resolver convention).
        self.warnings: list[str] = []

    @property
    def root(self) -> ContactFolder:
        return self._root

    def label(self) -> str:
        name = getattr(self._root, "display_name", None) or getattr(self._root, "id", "contacts")
        return f"contacts:{name}"

    # -- folders ---------------------------------------------------------------

    def _names(self, item: MigrationItem) -> tuple[str, list[str]]:
        """The source directory and the child folder names to create under the root.

        The export tree's first directory *is* the source folder the export started
        at, and the target folder plays that role on the way in — so it is dropped
        rather than recreated as a child of itself. Anything below it is a real
        subfolder, named from the exported ``folder_display_path``.
        """
        directory, _, _ = item.dest_path.rpartition("/")
        segments = [segment for segment in directory.split("/") if segment][1:]
        display = str((item.metadata or {}).get("folder_display_path") or "")
        names = [name for name in display.split("/") if name]
        if len(names) == len(segments) + 1:  # the display path still carries the root
            names = names[1:]
        if len(names) != len(segments):
            names = segments
        return directory, names

    def _folder(self, item: MigrationItem) -> tuple[str, ContactFolder]:
        directory, names = self._names(item)
        folder = self._folders.get(directory)
        if folder is None:
            folder = self._root
            for name in names:
                folder = folder.child_folders.ensure(name).execute_query()
            self._folders[directory] = folder
        return directory, folder

    # -- target contract -------------------------------------------------------

    def exists(self, item: MigrationItem) -> bool:
        """Whether an equal contact is already in the target folder.

        Matched on display name plus first address, because nothing the source knows
        survives the create. Duplicates *at the source* are honoured: the index keeps
        a list per key and each source item claims its own entry, so two contacts with
        the same name and address are still imported twice.
        """
        if item.dest_path in self._present:
            return True
        _, folder = self._folder(item)
        key = ContactRecord.from_json(item.metadata or {}).dedup_key
        claimed = self._claimed.get(key, 0)
        index = self._folder_index(folder)
        if claimed >= len(index.get(key) or []):
            return False
        self._claimed[key] = claimed + 1
        self._present[item.dest_path] = index[key][claimed]
        return True

    def write(self, item: MigrationItem, payload: Any) -> None:
        """Create the contact from its sidecar record.

        ``payload`` (the ``.vcf`` bytes) is deliberately unused: Graph's create body
        is the record's fields, and parsing the vCard would lose the office fields
        the export preserved precisely so this could be exact.
        """
        if item.item_type != "contact":
            raise ValueError(f"a contact folder imports contacts, not {item.item_type!r} ({item.dest_path})")
        record = ContactRecord.from_json(item.metadata or {})
        try:
            body = record.payload(self._options)
        except ValueError as e:
            raise ValueError(f"{item.dest_path}: {e}") from None
        _, folder = self._folder(item)
        collection = folder.contacts
        contact = collection.create_typed_object()
        collection.context.add_query(CreateEntityQuery(collection, body, contact))
        collection.context.execute_query()
        if "categories" in withheld(self._options) and record.to_json().get("categories"):
            self._categories_dropped += 1
        self._present[item.dest_path] = contact
        key = record.dedup_key
        self._folder_index(folder).setdefault(key, []).append(contact)
        self._claimed[key] = self._claimed.get(key, 0) + 1

    def list_paths(self) -> Iterable[str]:
        """The destination paths this target has created or recognised.

        A contact folder cannot be enumerated into export paths (the paths carry the
        source's name slug and id digest), so extras are not reported: presence
        verification covers what the plan expects, and the extras are contacts the
        user already had.
        """
        return sorted(self._present)

    def checksum(self, item: MigrationItem) -> str:
        """Fingerprint of the contact as the target folder returns it."""
        contact = self._present.get(item.dest_path)
        if contact is None or not contact.id:
            return ""
        _, folder = self._folder(item)
        # Read a fresh object through the folder the contact lives in: re-loading the
        # created one *appends* to its collection-valued properties (``emailAddresses``,
        # the phone lists, ``categories``), so the digest would see every list twice.
        read = folder.contacts[contact.id].select(list(ContactRecord.columns)).get().execute_query()
        return ContactRecord.of(read).digest(self._options)

    def commit(self, options: Any = None) -> None:  # noqa: ARG002 — runner hook signature
        """Report once what the run deliberately did not restore."""
        if self._categories_dropped:
            self.warnings.append(
                f"categories were left off {self._categories_dropped} contact(s): "
                "ContactImportOptions(restore_categories=False) asked for that"
            )

    # -- helpers ---------------------------------------------------------------

    def _folder_index(self, folder: ContactFolder) -> dict[tuple[str, str], list[Contact]]:
        """The folder's contacts, grouped by the key an import recognises."""
        directory = getattr(folder, "id", str(folder))
        cached = self._indexed.get(directory)
        if cached is None:
            index: dict[tuple[str, str], list[Contact]] = {}
            for contact in folder.contacts.select(_EXISTING_COLUMNS).get_all().execute_query():
                index.setdefault(ContactRecord.of(contact).dedup_key, []).append(contact)
            self._indexed[directory] = index
            cached = index
        return cached


__all__ = ["ContactSource", "ContactTarget", "VcfExportTarget", "VcfTreeSource"]
