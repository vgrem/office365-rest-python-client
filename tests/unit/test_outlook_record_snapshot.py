"""What an Outlook record yields -- a POST body, a document, a dedup key -- pinned.

The calendar and contact records are being rebuilt on the model's own declarations; this is
the guarantee that the rebuild changes nothing a service or a reader of the files can see.
The snapshot was captured from the implementation *before* this change, over every
combination of the import options -- that is, from ``96815900e`` plus the one-line fix this
change also carries: at that commit an event with no attendees and
``restore_attendees=True`` raised ``KeyError: 'attendees'``, so no snapshot could be
captured from it as it stood. Regenerating from that tree (``UPDATE_SNAPSHOT=1``)
reproduces this file byte for byte; a snapshot that cannot be regenerated from a named tree
is not a behaviour guarantee. The comparable form and its digest are not pinned: they
change by design, and ``test_comparable_profile.py`` and the import tests cover them as
properties (what the service rewrites compares equal, a real change does not).

Regenerate deliberately with ``UPDATE_SNAPSHOT=1`` and review the diff.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from pathlib import Path
from typing import Any, Callable

from office365.migration.outlook import (
    CalendarImportOptions,
    ContactImportOptions,
    ContactRecord,
    EventRecord,
)
from tests.unit.test_migration_calendar_import import _SERIES
from tests.unit.test_migration_calendar_import import _envelope as _event
from tests.unit.test_migration_contacts_import import _MINIMAL, _TWIN
from tests.unit.test_migration_contacts_import import _envelope as _contact

_SNAPSHOT = Path(__file__).parent / "snapshots" / "outlook_records.json"
_BOOLS = (False, True)


def _outcome(call: Callable[[], Any]) -> Any:
    """The value a call answers, or the error it raises: both are behaviour to preserve."""
    try:
        return call()
    except ValueError as error:
        return {"ValueError": str(error)}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _capture() -> dict[str, Any]:
    captured: dict[str, Any] = {}

    events = {
        "single": _event(),
        "series": _SERIES,
        "no_attendees": _event(attendees=[], categories=[]),
        "no_time": _event(start=None),
        "recurrence_text": _event(recurrence="PatternedRecurrence(...)"),
        "plain_body": _event(body={"contentType": "text", "content": "hello"}),
        "empty_body": _event(body={"contentType": "html", "content": ""}),
    }
    for name, envelope in events.items():
        if name != "recurrence_text":  # a legacy sidecar the codec was never meant to render
            captured[f"event.{name}.ics"] = _outcome(lambda e=envelope: _sha(EventRecord.from_json(e).ics()))
        for attendees, categories, transaction in itertools.product(_BOOLS, _BOOLS, _BOOLS):
            options = CalendarImportOptions(
                restore_attendees=attendees, restore_categories=categories, use_transaction_ids=transaction
            )
            label = f"event.{name}.a{int(attendees)}c{int(categories)}t{int(transaction)}"
            captured[f"{label}.payload"] = _outcome(lambda e=envelope, o=options: EventRecord.from_json(e).payload(o))
            captured[f"{label}.dropped"] = EventRecord.from_json(envelope).dropped_attendees(options)

    contacts = {
        "full": _contact(),
        "twin": _TWIN,
        "minimal": _MINIMAL,
        "unnamed": _contact(displayName="  "),
        "comma_category": _contact(categories=["a,b"]),
        "no_categories": _contact(categories=[]),
    }
    for name, envelope in contacts.items():
        record = ContactRecord.from_json(envelope)
        captured[f"contact.{name}.vcard"] = _sha(record.vcard())
        captured[f"contact.{name}.dedup"] = list(record.dedup_key)
        captured[f"contact.{name}.restored"] = record.restored()
        for categories in _BOOLS:
            options = ContactImportOptions(restore_categories=categories)
            captured[f"contact.{name}.c{int(categories)}.payload"] = _outcome(lambda r=record, o=options: r.payload(o))
    return json.loads(json.dumps(captured, sort_keys=True, default=str))


def test_records_yield_what_they_always_did():
    captured = _capture()
    if os.environ.get("UPDATE_SNAPSHOT"):
        _SNAPSHOT.parent.mkdir(exist_ok=True)
        _SNAPSHOT.write_text(json.dumps(captured, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    expected = json.loads(_SNAPSHOT.read_text(encoding="utf-8"))
    assert captured.keys() == expected.keys()
    drifted = sorted(key for key in expected if captured[key] != expected[key])
    assert not drifted, f"{len(drifted)} outputs changed, first: {drifted[:5]}"
