"""The declared-permission vocabulary: one model for checking, skipping and reporting.

These are decision tests: no tenant, no terminal, no network. ``TenantState.of`` is the
only door to the wire, so patching it keeps every other assertion about the logic the
decorators and the preflight report share.
"""

from __future__ import annotations

import types
import unittest
from unittest import TestCase, mock

from office365.outlook.mail.messages.message import Message
from office365.permissions import ResourceName
from office365.runtime.client_request_exception import ClientRequestException

from tests.capabilities import Needs, Requirement, TenantState, declared_calls
from tests.decorators import requires_call, requires_delegated
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase
from tests.preflight import ROOT, Grant, flow_of, grant_plan, needs_of
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

    def test_a_refused_lookup_is_not_reported_as_a_missing_permission(self):
        state = TenantState(unverifiable="the permission lookup needs a scope this token does not have")
        self.assertEqual(_MAIL.unmet(state), ["the permission lookup needs a scope this token does not have"])

    def test_a_name_the_api_does_not_publish_never_satisfies_the_group(self):
        """A directory records whatever string a grant names; the API is what decides."""
        requirement = Requirement(delegated=("BackupRestore.Read.All",))
        state = TenantState(delegated=frozenset({"BackupRestore.Read.All"}))
        self.assertEqual(
            requirement.unmet(state),
            [
                "delegated: any of BackupRestore.Read.All",
                "BackupRestore.Read.All is not a name Microsoft Graph publishes",
            ],
        )

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

    @requires_delegated("Mail.Read", bypass_roles=["Global Administrator"])
    def test_needs_mail_read(self):
        self.ran = True

    @requires_call(Message.send)
    def test_derives_its_scope_from_a_call(self):
        self.ran = True


class TestDecorators(TestCase):
    def test_a_derived_requirement_remembers_the_call_it_came_from(self):
        """The preflight row says which model methods asked for a grant; this is where it reads it."""
        calls = declared_calls(_Suite.test_derives_its_scope_from_a_call)
        self.assertEqual([call.rpartition(":")[2] for call in calls], ["Message.send"])
        self.assertEqual(declared_calls(_Suite.test_needs_mail_read), ())

    def test_a_missing_permission_is_named_in_the_skip_reason(self):
        case = _Suite()
        with mock.patch("tests.decorators.TenantState.of", return_value=TenantState()):
            with self.assertRaises(unittest.SkipTest) as caught:
                case.test_needs_mail_read()
        self.assertEqual(str(caught.exception), "missing delegated: any of Mail.Read")

    def test_a_test_without_a_client_is_skipped_not_failed(self):
        case = _Suite()
        case.client = None
        with self.assertRaises(unittest.SkipTest) as caught:
            case.test_derives_its_scope_from_a_call()
        self.assertIn("no client", str(caught.exception))


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
        plan = grant_plan([self._needs(requirement)], {requirement: TenantState()})
        self.assertEqual(plan, [Grant(flow="delegated", resource=ResourceName.Graph, names=("Mail.Read",))])

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


class TestSuiteMatrix(TestCase):
    def test_a_suite_signs_in_the_way_its_base_class_does(self):
        class ApplicationCase(GraphApplicationTestCase):
            pass

        class SharePointCase(SPTestCase):
            pass

        self.assertEqual(flow_of(ApplicationCase), "app-only")
        self.assertEqual(flow_of(GraphDelegatedTestCase), "delegated-ropc")
        self.assertEqual(flow_of(SharePointCase), "app-only-cert")
        self.assertIsNone(flow_of(TestCase))

    def test_an_offline_module_has_no_suite(self):
        module = types.ModuleType("fake_offline")

        class Plain(TestCase):
            def test_something(self):
                pass

        Plain.__module__ = module.__name__
        module.Plain = Plain
        self.assertIsNone(needs_of(ROOT / "tests/fake/test_offline.py", module))

    def test_an_unverified_requirement_is_not_reported_as_missing(self):
        needs = Needs(suite="tests/x/test_y.py", flow="delegated-ropc", tests=1)
        needs.add(_MAIL, "Suite.test_scoped")
        self.assertEqual(needs.unmet_for({}), [])
        self.assertEqual(needs.unmet_for({_MAIL: TenantState()}), [(_MAIL, ["Suite.test_scoped"])])
