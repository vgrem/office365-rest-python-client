"""One exported item: the model, its provenance, and the artefacts built from it.

An export writes two files per item — a portable payload (``.eml``, ``.ics``, ``.vcf``) and a
JSON sidecar — plus one ``manifest.jsonl`` for the run. The payload is what another client
opens. The sidecar is what an import replays, and it **is the model as the library
serializes it** (``entity.to_json()``) plus the three things no model can know: the folder
or calendar it came from, the file it is written to, and the display path a reader should
see. Nothing here lists a field, so a column a model gains is exported, replayed and
verified without a function being edited.

One class per family, whose class attributes *are* the declaration::

    class MessageRecord(SidecarRecord):
        model = Message
        content_suffix = ".eml"
        provenance = ("folder_path", "folder_display_path", "eml_path")
        identity = ("internet_message_id", "id")

A record answers the same questions built from a loaded model (:meth:`SidecarRecord.of`) or
read back from a sidecar (:meth:`SidecarRecord.from_json`): which identity the tree keys it
by, what the file is called, what an import posts, and what a verification compares. That is
what lets a family whose items are *fetched* (mail) and families whose items are *built*
(calendar, contacts) share one tree, one guard and one digest.

The model inside is hydrated on the library's own credential-less context, and it is never
handed out: a record is a document, so the only thing it can do with a service is render
one.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from datetime import datetime
from typing import Any, ClassVar, Dict, Iterable, Mapping, Sequence, Tuple, Type, TypeVar

from office365.migration.outlook.offline import offline_context
from office365.migration.outlook.restore import withheld
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.runtime.client_object import ClientObject
from office365.runtime.converters.value import serialize_value
from office365.runtime.odata.comparable import COMPARABLE, digest

#: A record of a specific family, so ``EventRecord.from_json(...)`` answers an ``EventRecord``.
_Record = TypeVar("_Record", bound="SidecarRecord")

#: How many provenance keys a sidecar carries.
_PROVENANCE_KEYS = 3

#: Filename stem cap. Well under every platform's 255-byte name limit, and long
#: enough to keep a subject recognizable next to its date and id digest.
MAX_SLUG_LENGTH = 60

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")
_RUNS = re.compile(r"-{2,}")


def slug(text: str | None) -> str:
    """A filesystem-safe, ASCII, length-capped rendering of a subject or a name.

    Used for a message subject, an event subject, a contact's display name and a
    folder name alike — hence :data:`MAX_SLUG_LENGTH` is a filesystem fact, not a
    service limit. Accented characters are folded to their ASCII base (``über`` ->
    ``uber``) rather than dropped, so two subjects differing only by accents do not
    collide; separators and punctuation collapse into single dashes.
    """
    if not text:
        return ""
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    stem = _UNSAFE.sub("-", folded).strip("-._")
    stem = _RUNS.sub("-", stem)
    return stem[:MAX_SLUG_LENGTH].strip("-._")


def dest_path(identity: str, folder_path: str, extension: str, stamp: str = "", label: str | None = None) -> str:
    """The one file-naming rule every Outlook export uses.

    ``<folder>/<stamp>_<label slug>_<identity digest><extension>``, absent parts left
    out. Deterministic, so a re-run finds the file it wrote; human-readable, so a
    calendar sorted by name reads chronologically; and the digest of the *identity*
    (not the label) keeps same-titled items on the same day apart — newsletters,
    ``RE:`` threads, ``(no subject)``, two meetings called ``Sync``.

    ``stamp`` is a date string (``""`` when the family has no date to sort by) and
    ``label`` is anything a human would recognise — a subject or a display name.
    """
    key = hashlib.sha1(identity.encode("utf-8")).hexdigest()[:8]
    stem = "_".join(part for part in (stamp, slug(label), key) if part)
    return f"{folder_path}/{stem}{extension}" if folder_path else f"{stem}{extension}"


def refuse_legacy_sidecar(envelope: Mapping[str, Any], keys: Iterable[str], family: str) -> None:
    """Refuse a sidecar written before the envelope was the model's own JSON.

    Naming the offending keys rather than saying "invalid sidecar": an operator who meets
    this needs to know it is the exporter's age, not a corrupt file. One rule, one row per
    family: the keys are the family's, the sentence is the code's.
    """
    found = [name for name in keys if name in envelope]
    if found:
        raise ValueError(
            f"this sidecar spells its own keys ({', '.join(found[:2])}) and was written by an older"
            f" exporter: re-export the {family} and import that tree"
        )


class SidecarRecord:
    """One item of an export: the model it came from, plus the keys no model answers.

    Subclassed once per family. The subclass sets class attributes and, where a family
    has an artefact of its own (a create body, a document, a dedupe key), the methods
    that render it; everything else here is derived from those attributes.
    """

    #: The model type this record speaks for.
    model: ClassVar[Type[ClientObject]]
    #: What the tree holds, as ``MigrationItem.item_type`` reports it.
    item_type: ClassVar[str] = "file"
    #: The payload file's extension.
    content_suffix: ClassVar[str] = ""
    #: The three keys a sidecar carries that no model does, in order: the folder it came
    #: from, the display path a reader should see, and the payload file it is written to.
    #: The only vocabulary a record owns — everything else is the model's.
    provenance: ClassVar[Tuple[str, ...]] = ()
    #: Keys a sidecar carried before it became the model's own JSON.
    legacy_keys: ClassVar[Tuple[str, ...]] = ()
    #: What :func:`refuse_legacy_sidecar` calls this family.
    legacy_name: ClassVar[str] = ""
    #: Model attributes naming the item, most stable first.
    identity: ClassVar[Tuple[str, ...]] = ("id",)
    #: Model attribute holding the part of the file name a human reads.
    label: ClassVar[str] = ""
    #: Model attributes holding the instant the file name sorts by, first set wins.
    file_stamp_from: ClassVar[Tuple[str, ...]] = ()
    #: Model attributes holding the audit stamps a migration item reports, first set wins.
    modified_from: ClassVar[Tuple[str, ...]] = ("last_modified_date_time",)
    created_from: ClassVar[Tuple[str, ...]] = ("created_date_time",)
    #: Model attributes a verification compares. Empty means every field the model sends
    #: — the ones the service owns are dropped by the profile either way.
    verified: ClassVar[Tuple[str, ...]] = ()
    #: Graph properties an export reads, so two exports of one source are comparable.
    columns: ClassVar[Sequence[str]] = ()
    #: The import options this family's artefacts default to.
    options_class: ClassVar[Type[Any]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        assert cls.provenance and len(cls.provenance) == _PROVENANCE_KEYS, (
            f"{cls.__name__}: a sidecar carries {_PROVENANCE_KEYS} provenance keys"
        )
        clash = set(cls.provenance) & set(cls.columns)
        assert not clash, f"{cls.__name__}: a provenance key collides with a declared column: {sorted(clash)}"

    def __init__(self, entity: ClientObject, envelope: Mapping[str, Any]) -> None:
        self._entity = entity
        self.envelope: Dict[str, Any] = dict(envelope)

    # -- construction ----------------------------------------------------------------

    @classmethod
    def of(
        cls: Type[_Record],
        entity: ClientObject,
        folder_path: str = "",
        display_path: str | None = None,
        extra_properties: Sequence[str] | None = None,
    ) -> _Record:
        """The record for an item read from the service: the model's JSON, plus provenance.

        All values are JSON-safe by construction — they came from a JSON response, went
        through ``to_json()`` and, for an extra property, through the library's own
        serializer — so nothing here is rescued later by ``json.dumps(..., default=str)``.
        """
        folder_key, display_key, payload_key = cls.provenance
        envelope = entity.to_json()
        envelope[folder_key] = folder_path
        envelope[display_key] = display_path or folder_path
        record = cls(entity, envelope)
        record.envelope[payload_key] = record.dest_path
        for name in extra_properties or []:
            record.envelope[name] = serialize_value(entity.get_property(name))
        return record

    @classmethod
    def from_json(cls: Type[_Record], envelope: Mapping[str, Any]) -> _Record:
        """The record a sidecar holds: read back into the model, with no service involved.

        Only the model's own names are hydrated: a provenance key is the export's
        bookkeeping, and a form built from a model that holds one would carry a field the
        model never declared.
        """
        refuse_legacy_sidecar(envelope, cls.legacy_keys, cls.legacy_name)
        declared = cls.model._schema.properties
        owned = {name: value for name, value in envelope.items() if name in declared}
        return cls(cls.model(offline_context()).hydrate(owned), envelope)

    # -- what the tree asks ----------------------------------------------------------

    def to_json(self) -> Dict[str, Any]:
        """The sidecar as it is written to disk."""
        return dict(self.envelope)

    @property
    def folder_path(self) -> str:
        """The folder or calendar the item was exported from, as it was spelled."""
        return str(self.envelope.get(self.provenance[0]) or "")

    @property
    def source_id(self) -> str:
        """The identity the tree keys the item by: the first :attr:`identity` the sidecar states."""
        return str(self._written(self.identity) or "")

    @property
    def id(self) -> str:
        """The Graph id the record is keyed by, or ``""`` when it has none."""
        return str(self._written(("id",)) or "")

    @property
    def dest_path(self) -> str:
        """Where the payload file is written: :func:`dest_path` over this record's own parts."""
        return dest_path(self.source_id, self.folder_path, self.content_suffix, self.file_stamp(), self.label_of())

    @property
    def modified(self) -> Any:
        """When the source last changed the item, in the spelling the service sent."""
        return self._written(self.modified_from)

    @property
    def created(self) -> Any:
        """When the item was created at the source, in the spelling the service sent."""
        return self._written(self.created_from)

    def file_stamp(self) -> str:
        """The date part of the file name; ``""`` when the family has no date to sort by."""
        return _date_of(self._first(self._entity, self.file_stamp_from))

    def label_of(self) -> str | None:
        """The part of the file name a human reads: a subject, or a display name."""
        return self._written((self.label,))

    # -- what a verification compares -------------------------------------------------

    def canonical(self, options: Any = None) -> Dict[str, Any]:
        """The restorable fields in the form the model says the service treats as equal.

        A field the import declines to restore (``restore_attendees``, ``restore_categories``)
        leaves the comparable form, which is why the source and the target of one job must
        share the options object.
        """
        options = self.options_class() if options is None else options
        return self._entity.to_json(COMPARABLE.scoped(self.model, only=self.verified or None, without=withheld(options)))

    def digest(self, options: Any = None) -> str:
        """A digest of the fields an import restores, for verifying that it did.

        Not the artefact's bytes: the other side of an import is the service, which
        assigns identifiers, re-formats what it is given and stamps its own instants, so
        the comparable artefact is the *item* — which fields take part is :attr:`verified`.
        """
        return digest(self.canonical(options))

    def checksum(self, payload: bytes, options: Any = None) -> str:
        """What a verification compares for this item, given the payload it was written to.

        A family whose bytes this package renders itself is checkable by them; one whose
        artefact the service re-serializes is not, and overrides this.
        """
        return self.digest(options)

    # -- helpers ---------------------------------------------------------------------

    def _written(self, attrs: Iterable[str]) -> Any:
        """The first of ``attrs`` the sidecar states, spelled as the exporter wrote it.

        Read off the envelope rather than the model so a stamp keeps the offset the
        service sent (``…Z``) instead of being re-rendered here.
        """
        return self._first(self.envelope, attrs, key=self.model.wire_name)

    @staticmethod
    def _first(source: Any, attrs: Iterable[str], key: Any = None) -> Any:
        """The first of ``attrs`` whose value ``source`` states — an attribute, or a key."""
        for attr in attrs:
            value = source.get(key(attr)) if key is not None else getattr(source, attr, None)
            if value:
                return value
        return None


def _date_of(value: Any) -> str:
    """A wall clock or an instant as the ``YYYY-MM-DD`` a file name sorts by."""
    moment = value.as_datetime() if isinstance(value, DateTimeTimeZone) else value
    return moment.strftime("%Y-%m-%d") if isinstance(moment, datetime) and moment != datetime.min else ""


__all__ = ["MAX_SLUG_LENGTH", "SidecarRecord", "dest_path", "refuse_legacy_sidecar", "slug"]
