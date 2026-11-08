"""The contact's vCard: the golden bytes, the omission rule, and the fold.

Contacts had no test at all. The vCard is what an export hands to a client that is not
Outlook, and the writer's contract *is* the document it produces, so it is compared byte
for byte against a fixture rather than field by field: line order, escaping, folding at 75
octets and the ``X-MS-`` extensions are all in the diff or in neither.

The sidecar beside each golden is what an import reads back, so the fixture is a record —
a sidecar plus provenance — and not a bare model: a contact rendered from a model the
service just returned and one re-read from disk on another machine must produce the same
bytes, which is the whole reason the sidecar exists.
"""

from __future__ import annotations

from office365.migration.outlook.contacts_models import ContactRecord
from tests.unit.outlook_fixtures import document, sidecar


def test_the_writer_renders_the_golden_document():
    """One assertion for every branch: N/ADR slots, escaped text, folded lines, a list."""
    assert ContactRecord.from_json(sidecar("contact")).vcard() == document("contact.vcf")


def test_an_unset_value_leaves_no_line():
    """A contact with a name and an id renders four lines, not twenty empty ones."""
    rendered = document("contact_minimal.vcf")
    assert ContactRecord.from_json(sidecar("contact_minimal")).vcard() == rendered
    lines = rendered.decode("utf-8").splitlines()
    assert lines == ["BEGIN:VCARD", "VERSION:3.0", "N:;;;;", "FN:Grace Hopper", "UID:c2", "END:VCARD"]
