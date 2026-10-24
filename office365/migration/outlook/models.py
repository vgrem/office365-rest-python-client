"""Mail records — the options, the per-message sidecar, and the MIME digest.

An exported message is two files: the RFC 822 bytes (``.eml``) and a JSON sidecar
carrying what MIME does not (Graph ids, categories, read state, conversation). The
sidecar is the message as the model serializes it, plus provenance; the convention
itself is :class:`office365.migration.outlook.records.SidecarRecord`, and the naming
rule every Outlook family shares is :func:`office365.migration.outlook.records.dest_path`.
What is left here is what only mail has: its options, the 4 MB MIME import cap, and
:func:`mime_digest` — the one comparable form of a message, because the ``.eml`` is the
only artefact in this package with no model behind it.
"""

from __future__ import annotations

import email
import email.message
import email.policy
import email.utils
import hashlib
import re
from dataclasses import dataclass, field
from typing import Any, cast

from office365.migration.outlook.records import SidecarRecord
from office365.outlook.mail.messages.message import Message
from office365.runtime.odata.comparable import digest


@dataclass
class MailExportOptions:
    """What a mailbox export includes.

    Defaults are the honest ones for a migration: the whole folder tree, drafts
    included (a draft is content a user expects to find after the move).
    """

    include_subfolders: bool = True
    include_drafts: bool = True
    #: Name of the top folder in the export tree (``None`` uses the folder's own
    #: display name). Set it to keep a stable root when the source folder is
    #: renamed between runs.
    root_name: str | None = None
    #: Extra Graph message properties to record in the sidecar (camelCase names).
    #: Read with ``message.get_property(name)``; unknown names are recorded as None.
    extra_properties: list[str] = field(default_factory=list)


#: Graph caps a MIME import request at 4 MB (the base64 body is the payload), so
#: a larger message has to go through an upload session instead.
MAX_IMPORT_MIME_BYTES = 4 * 1024 * 1024


@dataclass
class MailImportOptions:
    """What a mailbox import restores beyond the MIME bytes.

    Flag replay costs one extra PATCH per message, and only when the value Graph
    chose differs from the exported one, so the defaults are on.
    """

    #: Re-apply the exported read state. Graph marks an imported message read, so
    #: this only writes when the export says unread.
    restore_read_state: bool = True
    #: Re-apply the exported Outlook categories (the label set a Gmail move maps
    #: onto by hand).
    restore_categories: bool = True
    #: Import everything under this folder, created when absent (``None`` imports
    #: straight into the target folder).
    root_name: str | None = None


#: The prefix Exchange prepends to an imported HTML body. It restates the charset
#: the MIME headers already carry, so it is serialization, not content.
_EXCHANGE_HTML_PREFIX = re.compile(rb'^<meta http-equiv="Content-Type" content="[^"]*">')


def _canonical_date(value: str | None) -> str | None:
    """A ``Date`` header as ISO-8601, so ``04 Mar`` and ``4 Mar`` compare equal."""
    try:
        return email.utils.parsedate_to_datetime(value).isoformat() if value else None
    except (TypeError, ValueError):
        return value


def _canonical_addresses(value: str | None) -> list[list[str]]:
    """An address header as ``[name, address]`` pairs (``[]`` when absent)."""
    return [[name, address] for name, address in email.utils.getaddresses([value])] if value else []


def _leaf_digest(part: email.message.Message) -> str:
    """A leaf part's decoded payload, minus the wrapper Exchange puts around an HTML body."""
    payload = cast("bytes", part.get_payload(decode=True) or b"")
    if part.get_content_type() == "text/html":
        payload = _EXCHANGE_HTML_PREFIX.sub(b"", payload, count=1)
    return hashlib.sha256(payload).hexdigest()


def mime_digest(data: bytes) -> str:
    """A content fingerprint of an RFC 822 message that survives a mailbox round trip.

    Exchange re-serializes an import — drops per-part ``MIME-Version``, reflows
    ``Content-Type`` parameters, rewrites ``Date``, prepends a ``<meta http-equiv=...>``
    tag to an HTML body — so a byte checksum cannot verify one. This digests decoded leaf
    payloads and semantic headers instead, and an imported copy can be compared with the
    ``.eml`` it came from.

    Built here rather than through :data:`COMPARABLE` because the input is not a model: the
    ``.eml`` arrives as bytes from ``$value``, so RFC 822 has no declarations to apply.
    Empty for an unparsable message, which verification reports as unverifiable rather
    than as a mismatch.
    """
    if not data:
        return ""
    try:
        message = email.message_from_bytes(data, policy=email.policy.SMTP)
        leaves = [
            [part.get_content_type(), part.get_filename(), _leaf_digest(part)]
            for part in message.walk()
            if not part.is_multipart()
        ]
    except Exception:  # noqa: BLE001 — an unparsable message has no comparable content
        return ""
    return digest(
        {
            "subject": message.get("Subject"),
            "message_id": message.get("Message-ID"),
            "date": _canonical_date(message.get("Date")),
            "from": _canonical_addresses(message.get("From")),
            "to": _canonical_addresses(message.get("To")),
            "cc": _canonical_addresses(message.get("Cc")),
            "parts": leaves,
        }
    )


#: Keys a sidecar carried before it became the model's own JSON (see
#: :func:`office365.migration.outlook.records.refuse_legacy_sidecar`).
LEGACY_KEYS = (
    "graph_id",
    "internet_message_id",
    "sender",
    "received",
    "sent",
    "is_read",
    "is_draft",
    "has_attachments",
    "conversation_id",
    "parent_folder_id",
)


class MessageRecord(SidecarRecord):
    """One message as the export records it: the model's own JSON, plus provenance.

    A mailbox export writes the RFC 822 bytes as the payload and this record beside them,
    so an import replays what MIME cannot carry — the Graph id, read state, categories,
    the conversation — from Graph's own spellings (``receivedDateTime``, ``isRead``,
    ``internetMessageId``), which is also what the import reads back.

    The comparable form is :func:`mime_digest` rather than a digest of the fields: what an
    import promises is the *message*, and Exchange re-serializes it on the way in.
    """

    model = Message
    item_type = "file"
    content_suffix = ".eml"
    provenance = ("folder_path", "folder_display_path", "eml_path")
    legacy_keys = LEGACY_KEYS
    legacy_name = "mailbox"
    #: ``internetMessageId`` is the header-preserved identity, stable across mailboxes; a
    #: draft has none until it is sent, and a moved draft gets a new Graph id — which a
    #: re-run reports as a second copy rather than silently overwriting.
    identity = ("internet_message_id", "id")
    label = "subject"
    #: ``received`` is what a reader means by "when it arrived"; a draft has none until it
    #: is sent, hence the fallback. The audit stamps fall back the same way, because a mail
    #: item's instants are the only ones Exchange offers.
    file_stamp_from = ("received_date_time", "sent_date_time")
    modified_from = ("last_modified_date_time", "received_date_time", "sent_date_time")
    created_from = ("received_date_time", "sent_date_time")
    columns = (
        "id",
        "internetMessageId",
        "subject",
        "receivedDateTime",
        "sentDateTime",
        "lastModifiedDateTime",
        "isRead",
        "isDraft",
        "importance",
        "categories",
        "hasAttachments",
        "conversationId",
        "parentFolderId",
        "from",
        "toRecipients",
        "ccRecipients",
    )
    options_class = MailImportOptions

    def checksum(self, payload: bytes, options: Any = None) -> str:
        """What a verification compares for a message: what it *says*, not its bytes."""
        return mime_digest(payload)


__all__ = [
    "LEGACY_KEYS",
    "MAX_IMPORT_MIME_BYTES",
    "MailExportOptions",
    "MailImportOptions",
    "MessageRecord",
    "mime_digest",
]
