"""Two questions about the whole tree, both of which a live run answers the wrong way.

A wrong permission name is invisible in a tenant: the request is refused, the harness reads
the refusal as "not granted", and the test skips - so a typo and a missing grant look the
same. And a missing declaration is invisible everywhere: no request fails, no report names
it. Both are answered here, offline, against the names each API's service principal
publishes and against the declarations the model methods carry.
"""

from __future__ import annotations

from unittest import TestCase

import office365
from office365.permissions import APPLICATION, DELEGATED, catalog, index

#: One walk of the tree, at import: what the library promises and where it still says nothing.
LIBRARY = index(office365)

#: Public operations that still name no permission, per service package. The map only shrinks:
#: a harvest lowers a number here, and a declaration removed anywhere raises one. Both
#: directions fail until the number is recorded, which is the point - a debt nobody writes down
#: is a debt nobody pays. ``outlook`` is absent because it is closed: it is the pilot for the
#: markers-before-consumers design, small enough to finish before scaling.
#:
#: The detector counts a method that *submits* a query (``add_query``, ``execute_query``,
#: ``execute_batch``) and skips one that merely builds a query and returns it, so these are a
#: floor: the real number is higher, never lower.
PENDING: dict[str, int] = {
    "backuprestore": 6,
    "booking": 2,
    "common": 1,
    "intune": 14,
    "planner": 3,
    "reports": 4,
    "security": 2,
    "sharepoint": 824,
    "subscriptions": 2,
    "todo": 4,
}


class TestTheRatchet(TestCase):
    def test_an_operation_that_names_no_permission_is_a_debt_that_only_shrinks(self):
        """Every public method that submits a request says what the tenant must grant.

        The debt is recorded rather than banned, because banning it today would mean either
        inventing every declaration by hand or deleting the ratchet. Recording it makes both
        directions fail: a new undeclared operation raises a count, and a declaration that
        disappears raises a count too, so nothing can be dropped without the number moving.
        """
        self.assertEqual(LIBRARY.debt(), PENDING, "declare the permission on the method, or record the new count")

    def test_a_declared_name_is_one_the_api_publishes(self):
        """A name is a grant only if the API that owns it offers it, and the tree can ask.

        ``office365/permissions/snapshots`` holds the names each service principal publishes,
        so a declaration cannot outlive the permission it names. Without this, a renamed or
        mistyped name reaches the tenant as a refusal, which the harness reports as "not
        granted" - the one failure a live suite cannot distinguish from a real gap.
        """
        unknown, unpublished = set(), []
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

        self.assertTrue(LIBRARY.declared(), "no declarations found - the index is empty, not the tree")
        self.assertEqual([], unpublished, "a declaration names a permission the API does not publish")
        self.assertEqual(set(), unknown, "no snapshot for this API: run scripts/gen_permission_catalog.py")
