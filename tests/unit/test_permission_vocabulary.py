"""What the tree declares, and whether the API it names agrees.

A live run cannot answer these: a misspelled permission is refused, and the harness reads the
refusal as "not granted", so a typo and a missing grant look identical; a declaration that is
missing fails nothing at all. A walk of the package is the only thing that sees either.
"""

from __future__ import annotations

import office365
from office365.capabilities import capabilities_of
from office365.communications.callrecords.collection import CallRecordCollection
from office365.outlook.mail.messages.message import Message
from office365.permissions import APPLICATION, DELEGATED, catalog, index, require_permission

#: One walk of the tree: what the library promises and where it still says nothing.
LIBRARY = index(office365)

#: Public operations that still name no permission, per service package. The map only shrinks: a
#: harvest lowers a number, and a declaration removed anywhere raises one, which is the point - a
#: debt nobody writes down is a debt nobody pays.
#:
#: These 19 are what a fill that read one table per operation, from the docs as published, could
#: not read, and neither reason is a judgement about which permission is *right*: fifteen name a
#: member the REST reference publishes no operation page for (``OnenotePage.preview``,
#: ``DeviceManagementIntent.assign``, ...); four are documented as ``Not supported.`` in every flow
#: (``NamedLocation.restore``, ``RecoveryJobBase.cancel``), which is the reference answering.
PENDING: dict[str, int] = {
    "copilot": 1,
    "directory": 5,
    "exchange": 1,
    "intune": 9,
    "onenote": 2,
    "outlook": 1,
}

#: Every operation that declares a licence, and the seat its own page names. One entry, because a
#: licence gate is a decision about what a tenant has to buy, not a line that slips in with a
#: harvest.
LICENSED: dict[str, tuple[str, ...]] = {
    "office365.search.entity:SearchEntity.query": ("SPE_E5",),
}


def test_every_requesting_method_names_the_permission_it_needs():
    assert LIBRARY.debt() == PENDING, "declare the permission on the method, or record the new count"


def test_every_declared_permission_is_one_the_api_publishes():
    """A name is a grant only if the API that owns it offers it.

    ``office365/permissions/snapshots`` holds the names each service principal publishes, so a
    declaration cannot outlive the permission it names.
    """
    unpublished, unknown = [], set()
    for operation in LIBRARY.declared():
        for requirement in operation.declaration.requirements():
            snapshot = catalog(requirement.resource)
            if snapshot is None:
                unknown.add(str(requirement.resource))
                continue
            for kind, names in ((DELEGATED, requirement.delegated), (APPLICATION, requirement.application)):
                unpublished += [
                    f"{requirement.resource} does not publish {kind} {name}"
                    for name in names
                    if not snapshot.publishes(name, kind)
                ]

    assert LIBRARY.declared(), "no declarations found - the index is empty, not the tree"
    assert unpublished == [], "a declaration names a permission the API does not publish"
    assert unknown == set(), "no snapshot for this API: run scripts/gen_permission_catalog.py"


def test_a_licence_gate_is_written_down_with_its_operation():
    """A licence is a packaging fact the docs state, named as the service spells it.

    ``SPE_E5`` is the SKU; ``Microsoft 365 E5`` is what the invoice calls it, and would match
    nothing ``subscribedSkus`` reports.
    """
    named: dict[str, set[str]] = {}
    for operation in LIBRARY.declared():
        for requirement in operation.declaration.requirements():
            if requirement.licenses:
                named.setdefault(operation.fqn, set()).update(requirement.licenses)

    actual = {key: tuple(sorted(names)) for key, names in named.items()}
    assert actual == LICENSED, "a licence gate is a decision: add it here with the operation it gates"
    for names in LICENSED.values():
        for name in names:
            assert name.isupper() and " " not in name, f"{name!r} is not the spelling subscribedSkus reports"


def test_an_override_that_names_nothing_keeps_the_base_declaration():
    class Base:
        @require_permission(application=["Sites.Read.All"])
        def read(self):
            """Read."""

    class Restated(Base):
        def read(self):
            """Read, restated without a declaration."""

    class Replaced(Base):
        @require_permission(application=["Sites.FullControl.All"])
        def read(self):
            """Read, with its own declaration."""

    assert capabilities_of(Restated).declarations["read"].application == ("Sites.Read.All",)
    assert capabilities_of(Replaced).declarations["read"].application == ("Sites.FullControl.All",)


def test_a_call_answers_its_own_declarations_and_limits():
    """One call answers everything declared about a member: scopes, licences, columns and limits."""
    collection = capabilities_of(CallRecordCollection)
    assert "get_direct_routing_calls" in collection.declarations
    assert collection.schema.columns == ()  # a collection has none: they belong to what it holds
    assert not collection.queries.supports("top")

    send = capabilities_of(Message.send)
    assert send.declarations["send"].delegated == ("Mail.Send",)
    assert send.schema is None and send.queries is None
