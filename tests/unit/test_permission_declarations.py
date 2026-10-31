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
