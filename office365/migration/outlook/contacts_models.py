"""Contact records — one contact's sidecar, and the artefacts a migration builds from it.

The sidecar *is* the contact as Graph spells it: ``Contact.to_json()`` already answers
every column the export selected, with the typed values flattened by the library's own
serialiser. This module therefore owns no field list. It owns three things:

* **provenance** — the folder the contact came from and the ``.vcf`` beside it, which
  a model cannot know;
* **the two normalisations Exchange forces on a round trip** (a birthday compares by
  date, an address-only email reads back named after itself);
* **the artefacts** — a POST body, a digest, a vCard.

A record is built *from* a model (``ContactRecord.of(contact, folder)``) or read back
from a sidecar (``ContactRecord.from_json(payload)``); either way the payload is the
contract, so a record can be re-read from disk with no client — which is what lets an
import verify a sidecar against a contact the service returned, on two machines, with
the same code. The convention itself is
:class:`office365.migration.outlook.records.SidecarRecord`, shared with the other families.

Three Exchange behaviours are measured, not assumed:

* **The whole contact is selectable in one ``$select``** — every column the model
  declares, so an export of N contacts is N content reads plus the folder walk.
* **A birthday is normalised to a fixed time of day.** ``1953-05-01T00:00:00Z`` and
  ``1953-05-01T11:59:00+00:00`` are both stored as, and read back as,
  ``1953-05-01 11:59:00+00:00`` — so the digest compares the *date*, and a replay
  may send back either form.
* **An ``emailAddresses`` entry sent without a ``name`` comes back with ``name`` set
  to the address**, so the digest compares ``name or address`` rather than failing
  every round trip on that fill-in.

A contact's **photo** is a sub-resource, and neither end is cheap: the ``contact``
entity does not expose a ``hasPhoto`` column on this endpoint (measured — it is not
in a full read), so finding out costs one ``GET /photo`` that 404s
(``ErrorItemNotFound``) per contact without one. Photos are therefore out of scope
and reported as such in the fidelity matrix, rather than probed for one request per
contact in a run that may have thousands.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from office365.migration.outlook.records import SidecarRecord
from office365.migration.outlook.restore import restores, withheld
from office365.outlook.contacts.contact import Contact
from office365.runtime.odata.canonical import FORMATS

#: Graph contact properties an export reads: every column the model declares. Derived
#: rather than listed, for the reason the calendar projection is: a hand-kept list drifts
#: from the getters that consume it, and a ``$select`` that omits a column is
#: indistinguishable from a contact that has no value for it.
CONTACT_COLUMNS = Contact.select_all()

#: What an import may replay: everything the model declares that the service does not own.
#: The ownership is the model's own statement (``@odata(readonly=True)``: the id, the folder
#: the contact was read from, the address Exchange derived, the audit stamps), so the
#: replay set is a projection of the same declarations the export selects — a column the
#: model gains is exported, replayed and verified without a function here changing, and the
#: export's own bookkeeping is excluded for the same reason: not being declared.
_RESTORED = frozenset(CONTACT_COLUMNS) - Contact._schema.readonly

#: The five components of a Graph ``physicalAddress`` in the order a vCard ``ADR`` line
#: renders them — ``pobox;extended;street;locality;region;code;country`` has two empty
#: leading components, so the order is stated rather than taken from the dict.
_ADR_PARTS = ("street", "city", "state", "postalCode", "countryOrRegion")
_ADDRESS_KEYS = ("businessAddress", "homeAddress", "otherAddress")


#: RFC 6350 §3.1 caps a content line at 75 octets; a continuation starts with a space.
_MAX_LINE_OCTETS = 75

#: Digits in a vCard ``REV`` stamp: ``YYYYMMDD`` + ``HHMMSS``.
_REV_DIGITS = 14

_VCARD_ESCAPED = re.compile(r"([\\;,])")
_NEWLINES = re.compile(r"\r?\n")


@dataclass
class ContactExportOptions:
    """What a contact export includes."""

    #: Name of the top folder in the export tree (``None`` uses the contact folder's
    #: own display name, slugified). Set it to keep a stable root across renames.
    root_name: str | None = None
    #: Walk the folder's child folders too. On by default: contact folders nest, and
    #: an export that silently dropped ``Vendors`` under ``Work`` would be a loss the
    #: fidelity matrix does not declare.
    include_subfolders: bool = True
    #: Extra Graph contact properties to record in the sidecar (camelCase names).
    extra_properties: list[str] = field(default_factory=list)


@dataclass
class ContactImportOptions:
    """What an import of an exported contact tree restores.

    Pass the *same* options object to both adapters of an import job: the source
    computes the content digest of what the target promises to restore, so the two
    sides have to agree on the fields to be comparable (see :meth:`ContactRecord.digest`).
    """

    #: Re-apply the category labels.
    restore_categories: bool = restores("categories", default=True)


def _address_of(entry: Any) -> str:
    """The lower-cased address of a sidecar's email entry, or ``""``."""
    return str((entry or {}).get("address") or "").strip().lower()


class ContactRecord(SidecarRecord):
    """One contact as the export records it: Graph's payload, where it came from, its artefacts.

    ``payload`` is the create body an import posts, ``digest`` what a verification compares
    on either side, and ``vcard`` the portable document. Built from a loaded contact with
    :meth:`~office365.migration.outlook.records.SidecarRecord.of`, or from a sidecar on disk
    with :meth:`~office365.migration.outlook.records.SidecarRecord.from_json`.
    """

    model = Contact
    item_type = "contact"
    content_suffix = ".vcf"
    provenance = ("folder_path", "folder_display_path", "vcf_path")
    label = "display_name"
    created_from = ("created_date_time", "last_modified_date_time")
    columns = CONTACT_COLUMNS
    options_class = ContactImportOptions

    @property
    def dedup_key(self) -> Tuple[str, str]:
        """Display name and first address: what a target recognises a re-run's work by.

        Matching on the name alone would merge two different people who happen to share
        one, and nothing else survives the create: Exchange assigns no
        ``internetMessageId``/``iCalUid`` equivalent, and a created contact's id is new.
        """
        entries = self._written(("email_addresses",)) or []
        addresses = sorted(address for address in (_address_of(entry) for entry in entries) if address)
        return (str(self._written((self.label,)) or "").strip().lower(), addresses[0] if addresses else "")

    def restored(self) -> Dict[str, Any]:
        """The fields an import replays: the model's payload minus what Exchange assigns."""
        return {key: value for key, value in self.envelope.items() if key in _RESTORED}

    def payload(self, options: ContactImportOptions | None = None) -> Dict[str, Any]:
        """The Graph ``POST /contacts`` body for this record.

        A contact has no ``transactionId``, so concurrency is handled by the target's own
        dedupe index rather than by the service.
        """
        options = self.options_class() if options is None else options
        left_out = {Contact.wire_name(attr) for attr in withheld(options)}
        body = {key: value for key, value in self.restored().items() if value and key not in left_out}
        display_name = str(body.get("displayName") or "").strip()
        if not display_name:
            raise ValueError("the sidecar record has no display name: Exchange rejects a contact without one")
        # Mandatory, and the sidecar may hold it unstripped — set last, from the value
        # this method validated.
        body["displayName"] = display_name
        # Measured: Exchange rejects the whole contact (``ErrorPropertyUpdate``, "Property
        # update did not succeed.") when one category carries a comma — the vCard separates
        # categories with it. Refuse with the offending name instead of failing opaquely,
        # and let the runner count this item as an error.
        bad = [name for name in body.get("categories") or [] if "," in str(name)]
        if bad:
            raise ValueError(f"a contact category cannot contain a comma: {bad[0]!r}")
        return body

    def vcard(self) -> bytes:
        """The contact as a vCard 3.0 document.

        A courtesy for other clients — the sidecar is what an import replays — but it is
        the portable artefact of an export, and because this module renders the bytes
        itself an export *can* be verified by them (unlike a mail import, where Exchange
        re-serialises everything it accepts).
        """
        contact = self.envelope
        name = [contact.get(part) for part in ("surname", "givenName", "middleName", "title", "generation")]
        lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            "N:" + ";".join(_vcard_escape(part) for part in name),
            "FN:" + _vcard_escape(contact.get("displayName")),
            "UID:" + _vcard_escape(contact.get("id")),
        ]
        _add(lines, "NICKNAME", contact.get("nickName"))
        _add(lines, "TITLE", contact.get("jobTitle"))
        _add(lines, "ROLE", contact.get("profession"))
        if contact.get("companyName") or contact.get("department"):
            org = [contact.get("companyName"), contact.get("department")]
            lines.append("ORG:" + ";".join(_vcard_escape(part) for part in org))
        _add(lines, "X-MS-OFFICE-LOCATION", contact.get("officeLocation"))
        for number in contact.get("businessPhones") or []:
            lines.append(f"TEL;TYPE=WORK,VOICE:{_vcard_escape(number)}")
        for number in contact.get("homePhones") or []:
            lines.append(f"TEL;TYPE=HOME,VOICE:{_vcard_escape(number)}")
        if contact.get("mobilePhone"):
            lines.append(f"TEL;TYPE=CELL:{_vcard_escape(contact['mobilePhone'])}")
        for email in contact.get("emailAddresses") or []:
            if email.get("address"):
                lines.append(f"EMAIL;TYPE=INTERNET:{_vcard_escape(email['address'])}")
        for im_address in contact.get("imAddresses") or []:
            lines.append(f"X-MS-IMADDRESS:{_vcard_escape(im_address)}")
        for side, kind in zip(_ADDRESS_KEYS, ("WORK", "HOME", "OTHER")):
            address = contact.get(side) or {}
            if any(address.get(part) for part in _ADR_PARTS):
                # The two empty leading components are ``pobox`` and ``extended``, which
                # Graph does not model.
                adr = ["", ""] + [_vcard_escape(address.get(part)) for part in _ADR_PARTS]
                lines.append(f"ADR;TYPE={kind}:" + ";".join(adr))
        birthday = FORMATS["date"](str(contact.get("birthday") or "").strip())
        if birthday:
            lines.append("BDAY:" + birthday)
        if contact.get("personalNotes"):
            lines.append("NOTE:" + _vcard_escape(contact["personalNotes"]))
        if contact.get("categories"):
            lines.append("CATEGORIES:" + ",".join(_vcard_escape(label) for label in contact["categories"]))
        _add(lines, "URL", contact.get("businessHomePage"))
        stamp = _vcard_stamp(contact.get("lastModifiedDateTime"))
        if stamp:
            lines.append("REV:" + stamp)
        lines.append("END:VCARD")
        return "".join(_vcard_fold(line) + "\r\n" for line in lines).encode("utf-8")


def _vcard_stamp(value: Any) -> str:
    """An ISO timestamp as a vCard ``REV`` value (``YYYYMMDDTHHMMSSZ``)."""
    if not value:
        return ""
    text = re.sub(r"[^0-9]", "", str(value))
    # A vCard REV is ``YYYYMMDDTHHMMSSZ``: the digits carry the instant, the zone is ours.
    stamp = text[:_REV_DIGITS]
    return stamp + "Z" if len(stamp) == _REV_DIGITS else ""


def _vcard_escape(value: Any) -> str:
    """Escape a vCard TEXT value (RFC 6350 §3.4): backslash, comma, semicolon, newline."""
    text = _VCARD_ESCAPED.sub(r"\\\1", str(value if value is not None else ""))
    return _NEWLINES.sub(r"\\n", text)


def _vcard_fold(line: str) -> str:
    """Fold a content line at 75 octets without splitting a UTF-8 sequence."""
    if len(line.encode("utf-8")) <= _MAX_LINE_OCTETS:
        return line
    chunks: List[str] = []
    current = ""
    for char in line:
        if len((current + char).encode("utf-8")) > _MAX_LINE_OCTETS:
            chunks.append(current)
            current = " " + char  # a continuation starts with a space and counts toward the octets
        else:
            current += char
    chunks.append(current)
    return "\r\n".join(chunks)


def _add(lines: List[str], name: str, value: Any) -> None:
    """Append ``NAME:value`` when the value is set."""
    if value:
        lines.append(f"{name}:{_vcard_escape(value)}")


__all__ = [
    "CONTACT_COLUMNS",
    "ContactExportOptions",
    "ContactImportOptions",
    "ContactRecord",
]
