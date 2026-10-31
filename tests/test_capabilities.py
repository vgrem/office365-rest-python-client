"""The declared-permission vocabulary: one model for checking, skipping and reporting.

These are decision tests: no tenant, no terminal, no network. ``TenantState.of`` is the
only door to the wire, so patching it keeps every other assertion about the logic the
decorators and the preflight report share.
"""

from __future__ import annotations

import types
import unittest
from unittest import TestCase, mock

from office365.runtime.client_request_exception import ClientRequestException

from tests import capabilities
from tests.capabilities import Needs, Requirement, TenantState, declared_requirement
from tests.decorators import requires_application, requires_delegated
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase
from tests.preflight import ROOT, grant_plan, needs_of
from tests.sharepoint.sharepoint_case import SPTestCase

_MAIL = Requirement(delegated=("Mail.Read",))


class TestRequirement(TestCase):
    def test_any_declared_scope_satisfies_the_group(self):
        requirement = Requirement(delegated=("Mail.Read", "Mail.ReadWrite"))
        state = TenantState(delegated=frozenset({"Mail.ReadWrite"}))
        self.assertEqual(requirement.unmet(state), [])

    def test_no_declared_scope_is_named_in_the_shortfall(self):
        requirement = Requirement(delegated=("Mail.Read", "Mail.ReadWrite"))
        self.assertEqual(requirement.unmet(TenantState()), ["delegated: any of Mail.Read, Mail.ReadWrite"])

    def test_scope_and_license_are_both_required(self):
        requirement = Requirement(delegated=("Mail.Read",), licenses=("SPE_E5",))
        granted = TenantState(delegated=frozenset({"Mail.Read"}))
        self.assertEqual(requirement.unmet(granted), ["license: any of SPE_E5"])

    def test_a_bypass_role_satisfies_the_whole_requirement(self):
        requirement = Requirement(delegated=("Mail.Read",), bypass_roles=("Global Administrator",))
        self.assertEqual(requirement.unmet(TenantState(roles=frozenset({"Global Administrator"}))), [])

    def test_a_bypass_role_also_covers_a_missing_role(self):
        requirement = Requirement(roles=("Teams Administrator",), bypass_roles=("Global Administrator",))
        self.assertEqual(requirement.unmet(TenantState(roles=frozenset({"Global Administrator"}))), [])

    def test_a_refused_lookup_is_not_reported_as_a_missing_permission(self):
        state = TenantState(unverifiable="the permission lookup needs a scope this token does not have")
        self.assertEqual(_MAIL.unmet(state), ["the permission lookup needs a scope this token does not have"])

    def test_an_undeclared_requirement_is_always_met(self):
        self.assertEqual(Requirement().describe(), "no declared permission")
        self.assertEqual(Requirement().unmet(TenantState()), [])

    def test_a_description_reads_as_one_sentence(self):
        self.assertEqual(
            Requirement(delegated=("Mail.Read",), bypass_roles=("Global Administrator",)).describe(),
            "delegated: any of Mail.Read or role: any of Global Administrator",
        )


class TestTenantState(TestCase):
    def test_only_the_declared_facts_are_fetched(self):
        """An app-only token has no /me, so a check that asks for a license breaks it."""
        app_role = types.SimpleNamespace(value="Sites.Read.All")
        with mock.patch.object(capabilities, "_cached_app_permissions", return_value=[app_role]):
            with mock.patch.object(capabilities, "_cached_delegated_permissions", side_effect=AssertionError("x")):
                with mock.patch.object(capabilities, "_cached_licenses", side_effect=AssertionError("/me")):
                    state = TenantState.of(object(), "client-id", Requirement(application=("Sites.Read.All",)))
        self.assertEqual(state.application, frozenset({"Sites.Read.All"}))
        self.assertEqual(state.unverifiable, "")

    def test_a_refused_lookup_becomes_unverifiable_rather_than_empty(self):
        with mock.patch("tests.capabilities._cached_directory_roles", side_effect=_refused()):
            state = TenantState.of(object(), "client-id", Requirement(roles=("Global Reader",)))
        self.assertIn("permission lookup needs a scope", state.unverifiable)
        self.assertEqual(state.roles, frozenset())


def _refused() -> ClientRequestException:
    return ClientRequestException("Forbidden")


class _Suite:
    """A test case stand-in: real ``skipTest``, but not collected by pytest."""

    client = object()
    skipTest = TestCase.skipTest

    def __init__(self):
        self.ran = False

    def setUp(self):
        """A helper the matrix test reads: nothing stamps an undeclared method."""

    @requires_delegated("Mail.Read", bypass_roles=["Global Administrator"])
    def test_needs_mail_read(self):
        self.ran = True

    @requires_application("Sites.Read.All")
    def test_needs_a_site_scope(self):
        self.ran = True


class TestDecorators(TestCase):
    def test_the_decorator_stamps_what_it_will_check(self):
        requirement = declared_requirement(_Suite.test_needs_mail_read)
        assert requirement is not None
        self.assertEqual(requirement.delegated, ("Mail.Read",))
        self.assertEqual(requirement.bypass_roles, ("Global Administrator",))

    def test_an_undecorated_test_declares_nothing(self):
        self.assertIsNone(declared_requirement(_Suite.setUp))

    def test_a_missing_permission_is_named_in_the_skip_reason(self):
        case = _Suite()
        with mock.patch("tests.decorators.TenantState.of", return_value=TenantState()):
            with self.assertRaises(unittest.SkipTest) as caught:
                case.test_needs_mail_read()
        self.assertEqual(str(caught.exception), "missing delegated: any of Mail.Read")

    def test_a_granted_permission_runs_the_test(self):
        case = _Suite()
        granted = TenantState(delegated=frozenset({"Mail.Read"}))
        with mock.patch("tests.decorators.TenantState.of", return_value=granted):
            case.test_needs_mail_read()
        self.assertTrue(case.ran)

    def test_a_test_without_a_client_is_skipped_not_failed(self):
        case = _Suite()
        case.client = None
        with self.assertRaises(unittest.SkipTest) as caught:
            case.test_needs_a_site_scope()
        self.assertIn("no client", str(caught.exception))


def _fake_module() -> types.ModuleType:
    module = types.ModuleType("fake_suite")

    class Suite(GraphDelegatedTestCase):
        def test_undeclared(self):
            pass

        @requires_delegated("Mail.Read")
        def test_scoped(self):
            pass

    Suite.__module__ = module.__name__
    module.Suite = Suite
    return module


class TestShortfall(TestCase):
    """The unmet groups as data, which is what a grant plan is built from."""

    def test_an_unmet_group_is_returned_with_the_names_it_accepts(self):
        requirement = Requirement(delegated=("Mail.Read", "Mail.ReadWrite"), licenses=("SPE_E5",))
        state = TenantState(delegated=frozenset({"Mail.ReadWrite"}))
        self.assertEqual(requirement.shortfall(state), [("license", ("SPE_E5",))])

    def test_a_bypass_role_or_a_refused_lookup_has_no_shortfall(self):
        requirement = Requirement(delegated=("Mail.Read",), bypass_roles=("Global Administrator",))
        self.assertEqual(requirement.shortfall(TenantState(roles=frozenset({"Global Administrator"}))), [])
        self.assertEqual(requirement.shortfall(TenantState(unverifiable="no scope to ask with")), [])


class TestGrantPlan(TestCase):
    """The plan an administrator is asked to approve: minimal, deduplicated, honest."""

    @staticmethod
    def _needs(*requirements: Requirement) -> Needs:
        needs = Needs(suite="tests/x/test_y.py", flow="delegated-ropc", tests=len(requirements))
        for index, requirement in enumerate(requirements):
            needs.add(requirement, f"Suite.test_{index}")
        return needs

    def test_one_name_per_unmet_group_is_enough(self):
        requirement = Requirement(delegated=("Mail.Read", "Mail.ReadWrite"))
        states = {requirement: TenantState()}
        self.assertEqual(grant_plan([self._needs(requirement)], states), {"delegated": ["Mail.Read"]})

    def test_a_name_shared_by_two_groups_is_only_asked_for_once(self):
        first = Requirement(delegated=("A.Read", "B.Read"))
        second = Requirement(delegated=("B.Read", "C.Read"))
        states = {first: TenantState(), second: TenantState()}
        self.assertEqual(grant_plan([self._needs(first, second)], states), {"delegated": ["B.Read"]})

    def test_groups_an_administrator_cannot_grant_are_still_reported(self):
        requirement = Requirement(licenses=("SPE_E5",))
        self.assertEqual(grant_plan([self._needs(requirement)], {requirement: TenantState()}), {"license": ["SPE_E5"]})

    def test_a_granted_or_unverified_requirement_asks_for_nothing(self):
        met = Requirement(delegated=("Mail.Read",))
        unknown = Requirement(delegated=("Files.Read",))
        states = {met: TenantState(delegated=frozenset({"Mail.Read"}))}
        self.assertEqual(grant_plan([self._needs(met, unknown)], states), {})


class TestSuiteMatrix(TestCase):
    def test_a_suite_is_read_off_the_tests_it_contains(self):
        needs = needs_of(ROOT / "tests/fake_suite/test_fake.py", _fake_module())
        assert needs is not None
        self.assertEqual(needs.suite, "tests/fake_suite/test_fake.py")
        self.assertEqual(needs.flow, "delegated-ropc")
        self.assertEqual(needs.tests, 2)
        self.assertEqual(list(needs.requirements), [_MAIL])
        self.assertEqual(needs.requirements[_MAIL], ["Suite.test_scoped"])

    def test_an_offline_module_has_no_suite(self):
        module = types.ModuleType("fake_offline")

        class Plain(TestCase):
            def test_something(self):
                pass

        Plain.__module__ = module.__name__
        module.Plain = Plain
        self.assertIsNone(needs_of(ROOT / "tests/fake/test_offline.py", module))

    def test_the_most_specific_base_decides_the_flow(self):
        class ApplicationCase(GraphApplicationTestCase):
            pass

        class SharePointCase(SPTestCase):
            pass

        from tests.preflight import flow_of

        self.assertEqual(flow_of(ApplicationCase), "app-only")
        self.assertEqual(flow_of(GraphDelegatedTestCase), "delegated-ropc")
        self.assertEqual(flow_of(SharePointCase), "app-only-cert")
        self.assertIsNone(flow_of(TestCase))

    def test_an_unverified_requirement_is_not_reported_as_missing(self):
        needs = Needs(suite="tests/x/test_y.py", flow="delegated-ropc", tests=1)
        needs.add(_MAIL, "Suite.test_scoped")
        self.assertEqual(needs.unmet_for({}), [])
        self.assertEqual(needs.unmet_for({_MAIL: TenantState()}), [(_MAIL, ["Suite.test_scoped"])])
