"""Every permission the tree declares, against the API that mints it.

A declaration names a permission; the API it names publishes its own vocabulary, and only that
vocabulary ends up in a token. A name the API never minted is therefore a grant the directory
faithfully records and no token ever carries: the call answers 403 while the declaration looks
satisfied, and the suite skips as though the grant were missing. Nothing offline can tell the two
apart, which is why this reads the service principals themselves - and why it needs an app-only
token, since reading another API's definition takes ``Application.Read.All`` as an app role.
"""

from __future__ import annotations

import office365
from office365.directory.permissions.guard import published_permissions
from office365.permissions import APPLICATION, DELEGATED, index

from tests.graph_case import GraphApplicationTestCase

#: One walk of the tree: every declared permission, wherever it was declared.
LIBRARY = index(office365)


class TestDeclaredPermissions(GraphApplicationTestCase):
    def test_1_every_declared_name_is_one_the_api_publishes(self):
        unpublished: list[str] = []
        for operation in LIBRARY.declared():
            for requirement in operation.declaration.requirements():
                published = published_permissions(self.client, requirement.resource)
                for kind, names in ((DELEGATED, requirement.delegated), (APPLICATION, requirement.application)):
                    unpublished += [
                        f"{operation.fqn}: {requirement.resource} does not publish {kind} {name}"
                        for name in names
                        if not published.publishes(name, kind)
                    ]

        self.assertTrue(LIBRARY.declared(), "no declarations found - the index is empty, not the tree")
        self.assertEqual([], unpublished, "a declaration names a permission the API does not publish")
