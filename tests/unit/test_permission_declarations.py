"""The model's permission declarations, and the vocabulary they share with the live tests.

A live test declares what it needs with ``@requires_delegated``; a model method declares
what its request needs with ``@require_permission``. Both are read, never called, and
both are now the same :class:`Requirement` - so one report can price a scope by the tests
it unblocks *and* by the endpoints it unlocks.

Nothing here sends a request: the declarations are facts about the source tree.
"""

from __future__ import annotations

import ast
import pathlib
from typing import cast
from unittest import TestCase

from office365.directory.permissions.require_permission import PermissionRequirement, require_permission
from office365.directory.permissions.requirement import Requirement
from tests.capabilities import TenantState, declared_requirement
from tests.decorators import requires_delegated

ROOT = pathlib.Path(__file__).resolve().parents[2] / "office365"


def _declarations() -> list[tuple[str, int, dict[str, ast.expr]]]:
    """Every ``@require_permission(...)`` site in the package, as (path, line, keywords).

    Read with :mod:`ast` rather than by importing, so the walk cannot execute model code
    and cannot be fooled by a decorator that only looks right at runtime.
    """
    found: list[tuple[str, int, dict[str, ast.expr]]] = []
    for path in ROOT.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            if name == "require_permission":
                keywords = {kw.arg: kw.value for kw in node.keywords if kw.arg is not None}
                found.append((str(path.relative_to(ROOT)), node.lineno, keywords))
    return found


def _stamped_on(method: object) -> PermissionRequirement:
    """The declaration a decorated method carries - read off the wrapper, never called."""
    return cast(PermissionRequirement, vars(method)["__required_permissions__"])


def _declared(keywords: dict[str, ast.expr]) -> PermissionRequirement:
    """The declaration a site makes, rebuilt from its list literals."""
    lists = {key: ast.literal_eval(value) for key, value in keywords.items() if isinstance(value, ast.List)}
    return PermissionRequirement(**lists)


#: Symbols that put a request on the wire. Derived by suffix and by the two methods a
#: query is submitted through, so a new query type is covered without editing a list.
_QUEUE_SUFFIXES = ("Query",)
_QUEUE_CALLS = frozenset({"add_query", "execute_query", "execute_batch"})


def _queues_a_request(method: ast.AST) -> bool:
    """Whether this method's body - not its annotations - produces a request.

    Nested defs count, because a closure that builds the query is still work the public
    method does. A request issued by calling another method does *not* count, so this
    detector under-reports rather than over-reports: it can never demand a declaration
    for a method that only delegates.
    """
    for statement in getattr(method, "body", []):
        for node in ast.walk(statement):
            name = node.attr if isinstance(node, ast.Attribute) else getattr(node, "id", "")
            if not name:
                continue
            if name in _QUEUE_CALLS or name.endswith(_QUEUE_SUFFIXES):
                return True
    return False


def _is_declared(method: ast.AST) -> bool:
    return any(
        isinstance(decorator, ast.Call)
        and (decorator.func.attr if isinstance(decorator.func, ast.Attribute) else decorator.func.id)
        == "require_permission"
        for decorator in getattr(method, "decorator_list", [])
    )


def _operations() -> list[tuple[str, str, bool]]:
    """(package, qualified name, declares something) for every method that queues a request."""
    found: list[tuple[str, str, bool]] = []
    for path in ROOT.rglob("*.py"):
        relative = path.relative_to(ROOT)
        package = relative.parts[0] if len(relative.parts) > 1 else "."
        for node in ast.parse(path.read_text()).body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found.append((package, node.name, node))
            elif isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        found.append((package, f"{node.name}.{child.name}", child))
    return [(package, name, _is_declared(method)) for package, name, method in found if _queues_a_request(method)]


#: Code that must not be asked to name a permission: a generic collection cannot know the
#: type it creates, the transport belongs to whoever called it, and the migration layer calls
#: model methods that declare for themselves.
OUT_OF_SCOPE = frozenset({"runtime", "migration", "."})


def _undeclared_by_package() -> dict[str, int]:
    """Public operations that name no permission, counted per service package.

    A method that declares nothing while the base class it delegates to declares the request
    is invisible here, so the count is a floor, not a census. Private helpers are left out:
    they are not an entry point, and the method that reaches them owns the declaration.
    """
    counted: dict[str, int] = {}
    for package, qualified, declared in _operations():
        if package in OUT_OF_SCOPE or declared or qualified.rsplit(".", 1)[-1].startswith("_"):
            continue
        counted[package] = counted.get(package, 0) + 1
    return counted


def _declared_owners() -> list[str]:
    """Every method or function carrying a declaration, as "path:Class.method"."""
    found: list[str] = []
    for path in ROOT.rglob("*.py"):
        for node in ast.parse(path.read_text()).body:
            members: list[tuple[str, ast.AST]]
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                members = [(node.name, node)]
            elif isinstance(node, ast.ClassDef):
                members = [
                    (f"{node.name}.{child.name}", child)
                    for child in node.body
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
            else:
                members = []
            found.extend(f"{path.relative_to(ROOT)}:{name}" for name, member in members if _is_declared(member))
    return found


#: Public operations that still name no permission, per service package. The map only
#: shrinks: a harvest lowers a number here, and a declaration removed anywhere raises one.
#: Both directions fail until the number is recorded, which is the point - a debt nobody
#: writes down is a debt nobody pays. ``outlook`` is absent because it is closed: it is the
#: pilot for the markers-before-consumers design, small enough to finish before scaling.
PENDING: dict[str, int] = {
    "backuprestore": 6,
    "booking": 2,
    "common": 1,
    "communications": 18,
    "directory": 63,
    "intune": 14,
    "onedrive": 64,
    "planner": 3,
    "reports": 4,
    "security": 6,
    "sharepoint": 2247,
    "subscriptions": 2,
    "teams": 21,
    "todo": 4,
}


class TestOneDeclaration(TestCase):
    def test_a_method_callable_under_both_flows_states_one_requirement_per_flow(self):
        declared = PermissionRequirement(delegated=["Sites.Read.All"], application=["Sites.ReadWrite.All"])

        flows = declared.requirements()

        self.assertEqual([flow.delegated for flow in flows], [("Sites.Read.All",), ()])
        self.assertEqual([flow.application for flow in flows], [(), ("Sites.ReadWrite.All",)])

    def test_a_directory_role_stands_in_for_the_scope_instead_of_adding_to_it(self):
        declared = PermissionRequirement(application=["Mail.Read"], directory_roles=["Global Administrator"])

        (flow,) = declared.requirements()

        self.assertEqual(flow.bypass_roles, ("Global Administrator",))
        self.assertTrue(flow.satisfied_by(TenantState(roles=frozenset({"Global Administrator"}))))
        self.assertTrue(flow.satisfied_by(TenantState(application=frozenset({"Mail.Read"}))))

    def test_the_declaration_is_read_without_calling_the_method(self):
        @require_permission(application=["Mail.Send"])
        def send() -> None:
            raise AssertionError("a method must not be called to learn what it declares")

        declared = _stamped_on(send)

        self.assertEqual([flow.application for flow in declared.requirements()], [("Mail.Send",)])

    def test_a_declaration_that_names_nothing_becomes_nothing(self):
        self.assertEqual(PermissionRequirement(notes="todo").requirements(), ())

    def test_a_test_and_a_method_state_the_same_type(self):
        @requires_delegated("Mail.Read")
        def a_live_test(self: object) -> None:
            raise AssertionError("a test must not be called to learn what it declares")

        @require_permission(delegated=["Mail.Read"])
        def a_model_method() -> None:
            raise AssertionError("a method must not be called to learn what it declares")

        self.assertIsInstance(declared_requirement(a_live_test), Requirement)
        self.assertIsInstance(_stamped_on(a_model_method).requirements()[0], Requirement)


class TestEveryDeclaration(TestCase):
    def test_every_declaration_becomes_a_requirement(self):
        declarations = _declarations()
        silent = [f"{path}:{line}" for path, line, keywords in declarations if not _declared(keywords).requirements()]

        self.assertTrue(declarations, "no declarations found - the walk is broken, not the tree")
        self.assertEqual(silent, [], "a declaration that names no flow and no role can never be checked")


class TestUndeclaredOperations(TestCase):
    def test_an_operation_that_names_no_permission_is_a_debt_that_only_shrinks(self):
        """Every public method that queues a request says what the tenant must grant.

        The debt is recorded rather than banned, because banning it today would mean either
        inventing 2,455 declarations or deleting the ratchet. Recording it makes both
        directions fail: a new undeclared operation raises a count, and a declaration that
        disappears raises a count too, so nothing can be dropped without the number moving.
        """
        self.assertEqual(
            _undeclared_by_package(),
            PENDING,
            "declare the permission on the method, or record the new count in PENDING",
        )

    def test_the_owner_of_a_request_is_public(self):
        """A private helper is reached through the method that owns the request, so it names nothing.

        ``Message._sibling_path`` used to carry ``Mail.ReadWrite`` while building no request
        at all - a declaration that no caller could ever satisfy or fail on, and one that a
        grant plan would have priced as if an endpoint needed it.
        """
        private = [owner for owner in _declared_owners() if owner.rsplit(".", 1)[-1].startswith("_")]

        self.assertEqual(private, [], "a declaration belongs on the public method that queues the request")
