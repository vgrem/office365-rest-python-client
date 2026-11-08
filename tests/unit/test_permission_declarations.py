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
#: is a debt nobody pays. Nine packages closed the map one harvest at a time - ``todo``,
#: ``planner``, ``subscriptions``, ``booking``, ``security``, ``reports``, ``backuprestore``,
#: ``common`` and ``outlook`` named every operation they own, and ``sharepoint`` closed it too:
#: all 2,224 of its public request-issuing operations declare.
#:
#: The map reopened on 2026-11-07 for one reason, not 741: ``generator/settings.graph.yaml``
#: switched ``generate_methods`` on, so a CSDL operation the model used to omit is now a method
#: that submits a request (740 of the 741 below are those new methods). Every entry is that
#: single decision seen per package - the
#: composition is ``onedrive`` 413 (workbook functions and their typed results), ``intune`` 77,
#: ``directory`` 74, ``reports`` 53, ``teams`` 32, ``security`` 30, ``communications`` 23,
#: ``outlook`` 11, ``common`` 6, ``onenote`` 5, ``partners`` 5, ``copilot`` 4, ``booking`` 3,
#: ``admin`` 2 and the single ones in ``backuprestore``, ``search`` and ``exchange``. The map
#: shrinks by harvesting, package by package, exactly as it grew before.
#:
#: The detector counts a method that *submits* a query (``add_query``, ``execute_query``,
#: ``execute_batch``) and skips one that merely builds a query and returns it, so these are a
#: floor: the real number is higher, never lower.
#: ``common`` and ``intune`` moved together: the beta Settings Catalog pass generated 14
#: operations under ``office365/intune`` and 8 under ``office365/common``, and every one of
#: them submits a request no permission is declared on yet. The rest of the tree is
#: unchanged, so the debt grew by exactly the operations that pass added.
#:
#: The last move changed the map without touching the total: 85 types that sit in a product
#: package were moved out of ``office365/common``, so four undeclared operations left it - two
#: for ``directory`` and two for ``admin``. ``common`` 14 -> 10, ``directory`` 74 -> 76,
#: ``admin`` 2 -> 4, and every other entry is the same number it was, because the count
#: follows the file and the file changed address.
PENDING: dict[str, int] = {
    "admin": 4,
    "backuprestore": 1,
    "booking": 3,
    "common": 10,
    "communications": 23,
    "copilot": 4,
    "directory": 76,
    "exchange": 1,
    "intune": 91,
    "onedrive": 413,
    "onenote": 5,
    "outlook": 11,
    "partners": 5,
    "reports": 53,
    "search": 1,
    "security": 30,
    "teams": 32,
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
