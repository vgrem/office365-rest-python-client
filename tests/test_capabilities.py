"""The declared-permission vocabulary: one model for checking, skipping and reporting.

These are decision tests: no tenant, no terminal, no network. ``TenantState.of`` is the
only door to the wire, so patching it keeps every other assertion about the logic the
decorators and the preflight report share.
"""

from __future__ import annotations

import types
import unittest
from unittest import TestCase, mock

from office365.permissions import ResourceName
from office365.runtime.client_request_exception import ClientRequestException

from tests import capabilities, preflight
from tests.capabilities import Needs, Requirement, TenantState, declared_requirement
from tests.decorators import requires_application, requires_delegated
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase
from tests.preflight import ROOT, Grant, grant_plan, needs_of
from tests.settings import Settings
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
        plan = grant_plan([self._needs(requirement)], states)
        self.assertEqual(plan, [Grant(flow="delegated", resource=ResourceName.Graph, names=("Mail.Read",))])

    def test_a_name_shared_by_two_groups_is_only_asked_for_once(self):
        first = Requirement(delegated=("A.Read", "B.Read"))
        second = Requirement(delegated=("B.Read", "C.Read"))
        states = {first: TenantState(), second: TenantState()}
        plan = grant_plan([self._needs(first, second)], states)
        self.assertEqual(plan, [Grant(flow="delegated", resource=ResourceName.Graph, names=("B.Read",))])

    def test_groups_an_administrator_cannot_grant_are_still_reported(self):
        requirement = Requirement(licenses=("SPE_E5",))
        plan = grant_plan([self._needs(requirement)], {requirement: TenantState()})
        self.assertEqual(plan, [Grant(flow="license", resource=ResourceName.Graph, names=("SPE_E5",))])
        self.assertEqual([grant.grantable for grant in plan], [False])

    def test_a_sharepoint_name_is_planned_on_the_sharepoint_principal(self):
        requirement = Requirement(application=("Sites.FullControl.All",), resource=ResourceName.SharePoint)
        plan = grant_plan([self._needs(requirement)], {requirement: TenantState()})
        self.assertEqual(len(plan), 1)
        self.assertEqual((plan[0].resource, plan[0].names), (ResourceName.SharePoint, ("Sites.FullControl.All",)))
        self.assertEqual(plan[0].label(), "application on Office 365 SharePoint Online")

    def test_a_granted_or_unverified_requirement_asks_for_nothing(self):
        met = Requirement(delegated=("Mail.Read",))
        unknown = Requirement(delegated=("Files.Read",))
        states = {met: TenantState(delegated=frozenset({"Mail.Read"}))}
        self.assertEqual(grant_plan([self._needs(met, unknown)], states), [])


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

    def test_a_property_named_like_a_test_is_not_a_test(self):
        module = types.ModuleType("fake_props")

        class TestWithProperty(GraphDelegatedTestCase):
            @property
            def test_site(self):
                return None

            def test_real(self):
                pass

        TestWithProperty.__module__ = module.__name__
        module.TestWithProperty = TestWithProperty
        needs = needs_of(ROOT / "tests/fake/test_props.py", module)
        assert needs is not None
        self.assertEqual(needs.tests, 1)

    def test_an_unverified_requirement_is_not_reported_as_missing(self):
        needs = Needs(suite="tests/x/test_y.py", flow="delegated-ropc", tests=1)
        needs.add(_MAIL, "Suite.test_scoped")
        self.assertEqual(needs.unmet_for({}), [])
        self.assertEqual(needs.unmet_for({_MAIL: TenantState()}), [(_MAIL, ["Suite.test_scoped"])])


class TestPreflightText(TestCase):
    """The terminal view: the blockers first, the satisfied rest as a count.

    The report (`--report`) stays a table of every suite by every requirement, and a
    person reading it wants one answer -- what is blocking the most tests. So the view
    deduplicates requirements, ranks them by the tests they unblock, spells the
    alternatives as a count, and turns 277 lines into 19.
    """

    def setUp(self):
        # Hermetic: no `.env`, no tenant, no credentials -- so every flow is unready and
        # nothing is verified, which is what the offline view is.
        patcher = mock.patch.object(preflight, "settings", Settings(tenant="contoso.onmicrosoft.com"))
        patcher.start()
        self.addCleanup(patcher.stop)

    @staticmethod
    def _needs(*requirements: Requirement, tests: int = 1) -> Needs:
        """A suite that declares ``requirements``, each carried by ``tests`` test names."""
        needs = Needs(suite="tests/x/test_y.py", flow="delegated-ropc", tests=tests * len(requirements))
        for index, requirement in enumerate(requirements):
            for case in range(tests):
                needs.add(requirement, f"Suite.test_{index}_{case}")
        return needs

    def test_the_requirement_blocking_the_most_tests_is_listed_first(self):
        narrow = Requirement(delegated=("Narrow.Read",))
        wide = Requirement(delegated=("Wide.Read",))
        found = [self._needs(narrow, tests=1), self._needs(wide, tests=8)]
        states = {narrow: TenantState(), wide: TenantState()}
        lines = preflight.Report(found, states).text().splitlines()
        self.assertLess(
            next(i for i, line in enumerate(lines) if "Wide.Read" in line),
            next(i for i, line in enumerate(lines) if "Narrow.Read" in line),
        )

    def test_a_met_requirement_collapses_to_a_count_until_all_is_asked_for(self):
        granted = Requirement(delegated=("Mail.Read",))
        refused = Requirement(delegated=("Files.Read",))
        found = [self._needs(granted, refused)]
        states = {granted: TenantState(delegated=frozenset({"Mail.Read"})), refused: TenantState()}
        report = preflight.Report(found, states)
        compact = report.text()
        self.assertIn("1 met, 1 missing", compact)
        self.assertNotIn("Mail.Read", compact)
        expanded = report.text(show_all=True)
        self.assertIn("Mail.Read", expanded)
        self.assertIn("1 test ", expanded)  # singular: "1 test", not "1 tests"

    def test_a_blocker_names_one_name_per_group_and_counts_the_alternatives(self):
        # The screen says what to grant; the report (`--all`) says everything that works.
        requirement = Requirement(delegated=("Sites.Read.All", "Sites.ReadWrite.All"), bypass_roles=("Global Reader",))
        text = preflight.Report([self._needs(requirement)], {}).text()
        self.assertIn("delegated: Sites.Read.All (+1) or an administrator role", text)
        self.assertNotIn("Sites.ReadWrite.All", text)
        expanded = preflight.Report([self._needs(requirement)], {}).text(show_all=True)
        self.assertIn("any of Sites.Read.All, Sites.ReadWrite.All", expanded)

    def test_the_screen_stops_at_a_screenful_and_counts_the_rest(self):
        requirements = [Requirement(delegated=(f"Scope{index}.Read",)) for index in range(preflight.Report.SHOWN + 2)]
        found = [self._needs(requirement) for requirement in requirements]
        states = dict.fromkeys(requirements, TenantState())
        lines = preflight.Report(found, states).text().splitlines()
        self.assertEqual(len([line for line in lines if "Scope" in line]), preflight.Report.SHOWN)
        self.assertIn("  ... 2 with fewer tests; --all spells every alternative", lines)
        everything = preflight.Report(found, states).text(show_all=True).splitlines()
        self.assertEqual(len([line for line in everything if "Scope" in line]), len(requirements))

    def test_a_flow_that_cannot_sign_in_says_which_setting_it_lacks(self):
        # `Settings()` names no client id, so the flow cannot sign in -- and silence
        # about that is how a skipped suite looks like a passing one.
        self.assertIn("delegated       not configured (missing: OFFICE365_CLIENT_ID)", preflight.Report([], {}).text())

    def test_the_screen_states_that_nothing_was_verified_without_verify(self):
        found = [self._needs(Requirement(delegated=("Mail.Read",)))]
        self.assertIn("not verified: --verify resolves them against this tenant", preflight.Report(found, {}).text())
        self.assertNotIn("not verified:", preflight.Report(found, {_MAIL: TenantState()}).text())

    def test_neither_view_uses_a_character_a_terminal_may_not_have(self):
        # No emoji, no box drawing, no colour: the same bytes in a terminal, a log and a
        # CI summary. Pinned because the compact view is what people read.
        found = [self._needs(Requirement(delegated=("Mail.Read",)))]
        report = preflight.Report(found, {})
        for view in (report.text(), report.text(show_all=True), report.markdown()):
            self.assertTrue(view.isascii(), view)
