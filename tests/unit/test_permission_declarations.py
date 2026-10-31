"""The permission declarations, the vocabulary they share with live tests, and the debt.

A model method declares what its request needs with ``@require_permission``; a live test either
declares its own precondition with ``@requires_delegated`` or derives it from the model with
``@requires_call(Message.send)``. Both are read, never called, and both become the same
:class:`Requirement` - so one report can price a scope by the tests it unblocks *and* by the
endpoints it unlocks.

Nothing here sends a request and nothing here reads source: declarations are read off the
methods that carry them, and the whole-package questions come from
:func:`office365.permissions.index`.
"""

from __future__ import annotations

from collections.abc import Coroutine
from typing import Any
from unittest import TestCase

import office365
from office365.permissions import (
    Index,
    PermissionRequirement,
    Requirement,
    ResourceName,
    declared,
    index,
    require_permission,
)
from tests.capabilities import TenantState, declared_requirement
from tests.decorators import requires_call, requires_delegated

#: One walk of the tree, at import: what the library promises and where it still says nothing.
#: The package imports itself module by module, so this is the only side effect in the file.
LIBRARY: Index = index(office365)


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
    "communications": 18,
    "directory": 61,
    "intune": 14,
    "onedrive": 61,
    "planner": 3,
    "reports": 4,
    "security": 2,
    "sharepoint": 2228,
    "subscriptions": 2,
    "teams": 21,
    "todo": 4,
}


class FakeQuery:
    """A query whose only relevant property is the tag a declaration writes on it."""

    permission_requirement: object = None


class FakeContext:
    """A runtime context reduced to what ``@require_permission`` touches."""

    def __init__(self) -> None:
        self.last_query: FakeQuery | None = None

    def add_query(self, query: FakeQuery) -> None:
        self.last_query = query


class FakeOwner:
    def __init__(self) -> None:
        self.context = FakeContext()

    @require_permission(delegated=["Mail.Send"], application=["Mail.Send"])
    def send(self) -> None:
        self.context.add_query(FakeQuery())

    @require_permission(delegated=["Mail.Send"], application=["Mail.Send"])
    def send_async(self) -> Coroutine[Any, Any, None]:
        async def run() -> None:
            self.context.add_query(FakeQuery())

        return run()

    @require_permission(delegated=["Mail.Read"], application=["Mail.Read"])
    def read_without_a_request(self) -> str:
        return "no query queued"


class TestOneDeclaration(TestCase):
    def test_a_method_callable_under_both_flows_states_one_requirement_per_flow(self):
        declaration = PermissionRequirement(delegated=("Sites.Read.All",), application=("Sites.ReadWrite.All",))

        flows = declaration.requirements()

        self.assertEqual([flow.delegated for flow in flows], [("Sites.Read.All",), ()])
        self.assertEqual([flow.application for flow in flows], [(), ("Sites.ReadWrite.All",)])

    def test_a_directory_role_stands_in_for_the_scope_instead_of_adding_to_it(self):
        declaration = PermissionRequirement(application=("Mail.Read",), directory_roles=("Global Administrator",))

        (flow,) = declaration.requirements()

        self.assertEqual(flow.bypass_roles, ("Global Administrator",))
        self.assertTrue(flow.satisfied_by(TenantState(roles=frozenset({"Global Administrator"}))))
        self.assertTrue(flow.satisfied_by(TenantState(application=frozenset({"Mail.Read"}))))

    def test_a_declaration_that_names_nothing_becomes_nothing(self):
        self.assertEqual(PermissionRequirement(notes="todo").requirements(), ())

    def test_a_declaration_names_microsoft_graph_unless_it_says_otherwise(self):
        """A name means one API's grant, so the API is part of the declaration.

        The default is the one 184 declarations already mean, which keeps Graph methods from
        having to say what the whole library said before; the ones that do not mean it say so.
        """
        self.assertEqual(PermissionRequirement(delegated=("Mail.Read",)).resource, ResourceName.Graph)
        self.assertEqual(
            PermissionRequirement(delegated=("AllSites.FullControl",), resource=ResourceName.SharePoint).resource,
            ResourceName.SharePoint,
        )

    def test_a_requirement_keeps_the_resource_of_its_declaration(self):
        declaration = PermissionRequirement(delegated=("AllSites.FullControl",), resource=ResourceName.SharePoint)

        (requirement,) = declaration.requirements()

        self.assertEqual(requirement.resource, ResourceName.SharePoint)
        self.assertEqual(
            requirement.unmet(TenantState(delegated=frozenset({"Sites.ReadWrite.All"}))),
            ["delegated on Office 365 SharePoint Online: any of AllSites.FullControl"],
        )

    def test_a_test_and_a_method_state_the_same_type(self):
        @requires_delegated("Mail.Read")
        def a_live_test(self: object) -> None:
            raise AssertionError("a test must not be called to learn what it declares")

        @require_permission(delegated=["Mail.Read"])
        def a_model_method() -> None:
            raise AssertionError("a method must not be called to learn what it declares")

        self.assertIsInstance(declared_requirement(a_live_test), Requirement)
        self.assertIsInstance(declared(a_model_method).requirements()[0], Requirement)


class TestTheMarker(TestCase):
    """What ``@require_permission`` does besides recording the names."""

    def test_the_declaration_is_read_without_calling_the_method(self):
        @require_permission(application=["Mail.Send"])
        def send() -> None:
            raise AssertionError("a method must not be called to learn what it declares")

        self.assertEqual(declared(send).application, ("Mail.Send",))


class TestEveryDeclaration(TestCase):
    def test_every_declaration_becomes_a_requirement(self):
        declarations = LIBRARY.declared()
        silent = [
            operation.qualname
            for operation in declarations
            if operation.declaration is None or not operation.declaration.requirements()
        ]

        self.assertTrue(declarations, "no declarations found - the index is empty, not the tree")
        self.assertEqual(silent, [], "a declaration that names no flow and no role can never be checked")


class TestUndeclaredOperations(TestCase):
    def test_an_operation_that_names_no_permission_is_a_debt_that_only_shrinks(self):
        """Every public method that submits a request says what the tenant must grant.

        The debt is recorded rather than banned, because banning it today would mean either
        inventing 2,437 declarations or deleting the ratchet. Recording it makes both
        directions fail: a new undeclared operation raises a count, and a declaration that
        disappears raises a count too, so nothing can be dropped without the number moving.
        """
        self.assertEqual(LIBRARY.debt(), PENDING, "declare the permission on the method, or record the new count")

    def test_the_owner_of_a_request_is_public(self):
        """A private helper is reached through the method that owns the request, so it names nothing.

        ``Message._sibling_path`` used to carry ``Mail.ReadWrite`` while building no request at
        all - a declaration that no caller could ever satisfy or fail on, and one that a grant
        plan would have priced as if an endpoint needed it.
        """
        private = [operation.qualname for operation in LIBRARY.declared() if operation.is_private]

        self.assertEqual(private, [], "a declaration belongs on the public method that owns the request")

    def test_an_operation_is_either_declared_or_counted_as_debt(self):
        undeclared = {operation.fqn for operation in LIBRARY.undeclared()}
        declared_names = {operation.fqn for operation in LIBRARY.declared()}

        self.assertEqual(undeclared & declared_names, set())
        self.assertEqual(undeclared | declared_names, {operation.fqn for operation in LIBRARY.operations})


class TestDerivedRequirement(TestCase):
    """A test can read what the method it calls declares instead of restating it.

    ``@requires_call`` is the consumer side of the declarations: the live suite stops naming
    scopes that the model already names, and a disagreement between the two becomes an edit in
    one place rather than a drift between two.
    """

    @staticmethod
    def _call(**declared_scopes: list[str]) -> object:
        """A model method carrying a real declaration, which fails if anything calls it."""

        @require_permission(**declared_scopes)
        def model_method(self: object) -> None:
            raise AssertionError("a declaration is read from the method, the method is not called")

        return model_method

    def test_a_test_needs_what_the_method_it_calls_declares(self):
        call = self._call(delegated=["Mail.Read"], application=["Mail.Read.All"])

        @requires_call(call)  # type: ignore[arg-type]
        def test_something(self) -> None:
            raise AssertionError("the decorator only stamps; the test body is never reached")

        self.assertEqual(declared_requirement(test_something), Requirement(delegated=("Mail.Read",)))

    def test_two_calls_are_conjoined_rather_than_alternated(self):
        send = self._call(delegated=["Mail.Send"])
        read = self._call(delegated=["Mail.Read", "Mail.Send"])

        @requires_call(send, read)  # type: ignore[arg-type]
        def test_something(self) -> None:
            return None

        self.assertEqual(declared_requirement(test_something), Requirement(delegated=("Mail.Send", "Mail.Read")))

    def test_the_flow_follows_the_test_not_the_method(self):
        call = self._call(delegated=["Mail.Read"], application=["Mail.Read.All"])

        @requires_call(call, flow="application")  # type: ignore[arg-type]
        def test_something(self) -> None:
            return None

        self.assertEqual(declared_requirement(test_something), Requirement(application=("Mail.Read.All",)))

    def test_a_role_the_declaration_names_can_bypass_the_whole_requirement(self):
        call = self._call(delegated=["Sites.FullControl.All"], directory_roles=["SharePoint Administrator"])

        @requires_call(call, bypass_roles=["Global Administrator"], require_licenses=["SPE_E5"])  # type: ignore[arg-type]
        def test_something(self) -> None:
            return None

        self.assertEqual(
            declared_requirement(test_something),
            Requirement(
                delegated=("Sites.FullControl.All",),
                licenses=("SPE_E5",),
                bypass_roles=("Global Administrator", "SharePoint Administrator"),
            ),
        )

    def test_a_method_that_declares_nothing_cannot_be_derived_from(self):
        def undeclared(self: object) -> None:
            return None

        with self.assertRaisesRegex(ValueError, "names no permission"):
            requires_call(undeclared)

    def test_a_method_that_declares_nothing_under_the_tests_flow_is_a_loud_error(self):
        call = self._call(application=["Mail.Read.All"])

        with self.assertRaisesRegex(ValueError, "declares no delegated permission"):
            requires_call(call)  # type: ignore[arg-type]

    def test_joins_refuse_to_build_an_empty_requirement(self):
        with self.assertRaisesRegex(ValueError, "at least one declaration"):
            Requirement.join()

    def test_two_apis_cannot_be_joined_into_one_requirement(self):
        """Merging two APIs' names would produce a group of names that do not compare."""
        graph = self._call(delegated=["Mail.Read"])
        sharepoint = self._call(delegated=["AllSites.FullControl"], resource=ResourceName.SharePoint)

        with self.assertRaisesRegex(ValueError, "one API resource"):
            requires_call(graph, sharepoint)  # type: ignore[arg-type]

    def test_a_derived_requirement_carries_the_resource_it_was_derived_on(self):
        sharepoint = self._call(delegated=["AllSites.FullControl"], resource=ResourceName.SharePoint)

        @requires_call(sharepoint)  # type: ignore[arg-type]
        def test_something(self) -> None:
            return None

        requirement = declared_requirement(test_something)
        assert requirement is not None
        self.assertEqual(requirement.resource, ResourceName.SharePoint)

    def test_a_join_of_roles_only_is_still_a_requirement(self):
        call = self._call(directory_roles=["Global Administrator"])

        self.assertEqual(Requirement.join(declared(call)), Requirement(bypass_roles=("Global Administrator",)))
