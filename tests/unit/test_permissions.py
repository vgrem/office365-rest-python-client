"""The declared-permission vocabulary: what the tree declares, and what a test does with it.

These are decision tests: no tenant, no terminal, no network. ``TenantState.of`` is the only
door to the wire, so patching it keeps every assertion about the logic the decorators and the
preflight report share.

The first half asks what a declaration means to one test -- a requirement is met by any of its
scopes, a role bypasses it, an unreadable lookup is not a missing permission -- and what the
harness then does: skip, or report what an administrator would have to grant. The second half
asks the same question of the tree at once: every requesting method names its permission, every
plan name is one Microsoft publishes, and a paid family names the licence that carries it.

A live run cannot answer the second half. A declaration that is missing fails nothing, because
a call without a declared permission is simply a call, and the grant it silently relied on looks
like an unused one; a misspelt plan matches nothing ``subscribedSkus`` reports and refuses every
call. A walk of the package is the only thing that sees either, which is why the two halves are
one file: the walk and the harness are the same vocabulary read at two distances.

Whether a declared *name* exists is the other question, and it is asked where a tenant is: the
API's own service principal is the only authority for what it publishes. That check lives in
``tests/graph/test_declared_permissions.py``.

A licence is the third vocabulary, and it has an authority that is not a tenant: Microsoft
publishes the service plan names, so a marker can be spelled-checked against the published list
without a call. ``tests/data/service_plans.txt`` is that list, refreshed by
``python scripts/fetch_service_plans.py``.
"""

from __future__ import annotations

import ast
import importlib
import pathlib
import types
import unittest
from unittest import TestCase, mock

import office365
from office365.capabilities import capabilities_of
from office365.communications.callrecords.collection import CallRecordCollection
from office365.outlook.mail.messages.message import Message
from office365.permissions import Catalog, ResourceName, index, require_permission
from office365.permissions.declaration import licence_of
from office365.runtime.client_request_exception import ClientRequestException
from tests.capabilities import Needs, Requirement, TenantState, declared_calls
from tests.decorators import requires_call, requires_delegated
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase
from tests.preflight import ROOT, Grant, flow_of, grant_plan, needs_of
from tests.sharepoint.sharepoint_case import SPTestCase

_MAIL = Requirement(delegated=("Mail.Read",))


# --- what a declaration means for one requirement -------------------------------------


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
        state = TenantState(
            delegated=frozenset({"BackupRestore.Read.All"}),
            published=Catalog(delegated=frozenset({"Mail.Read"})),
        )
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


# --- what a suite does with it -------------------------------------------------------


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


# --- what an administrator is asked for -----------------------------------------------


class TestGrantPlan(TestCase):
    """The plan an administrator is asked to approve: minimal, deduplicated, honest."""

    @staticmethod
    def _needs(*requirements: Requirement) -> Needs:
        needs = Needs(suite="tests/x/test_y.py", flow="delegated-ropc", tests=len(requirements))
        for number, requirement in enumerate(requirements):
            needs.add(requirement, f"Suite.test_{number}")
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


# --- how a suite is classified -------------------------------------------------------


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


# --- what the tree declares, asked once of every module -------------------------------


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
#:
#: ``sharepoint`` is the other way round, and the only entry no harvest produced: not one module
#: under ``office365/sharepoint`` declares a permission, so the product carries no debt until an
#: operation arrives -- ``SPARK.get_embedding`` and the four that came with it are the first five,
#: and ``Sites.*`` would be a guess, not a declaration.
PENDING: dict[str, int] = {
    "copilot": 1,
    "directory": 5,
    "exchange": 1,
    "intune": 9,
    "onenote": 2,
    "outlook": 1,
    "sharepoint": 5,
}

#: The service plan names Microsoft publishes for licensing. A marker is a claim about what a
#: tenant bought, and the vocabulary is the service's, so a misspelt plan is not a strictness
#: question: it matches nothing ``subscribedSkus`` reports and refuses every call.
SERVICE_PLANS: frozenset[str] = frozenset(
    line.strip()
    for line in (pathlib.Path(__file__).resolve().parents[1] / "data" / "service_plans.txt")
    .read_text(encoding="utf-8")
    .splitlines()
    if line.strip() and not line.startswith("#")
)

#: Families that sell a capability, and so are expected to say which licence carries it. The tree
#: at large is free - ``sharepoint``, ``onedrive``, ``teams`` and their neighbours cost a seat, not
#: a capability - so the claim is made where a product is sold rather than everywhere.
PAID: frozenset[str] = frozenset(
    {
        "intune",
        "directory.identitygovernance",
        "directory.synchronization",
        "directory.rolemanagement",
        "directory.protection",
        "security.ediscovery",
        "security.labels",
        "backuprestore",
    }
)

#: The types in those families that declare a permission and name no licence, each group with the
#: reason. A stamp that is wrong refuses a tenant that paid, which is worse than the 403 it was
#: explaining, so silence is the answer wherever one name would be false for another buyer.
#:
#: A family that gets stamped disappears from here; a declaring type that arrives in one of these
#: families fails this test until someone decides which it is. That is the whole ratchet: the
#: ``intune`` sweep was 66 types, and three of them - the PIM schedule requests and the risky-user
#: collection - were stamped by this list rather than by the sweep.
SILENT: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Lifecycle workflows and the consent-request queues ship with Entra ID Governance, whose plan is "
        "published as Entra_Identity_Governance. No tenant here reports it, so a marker could name it and "
        "nothing would show the name was the missing thing rather than the grant.",
        (
            "office365.directory.identitygovernance.appconsent.request_collection:AppConsentRequestCollection",
            "office365.directory.identitygovernance.insights:Insights",
            "office365.directory.identitygovernance.task_processing_result:TaskProcessingResult",
            "office365.directory.identitygovernance.userconsent.request_collection:UserConsentRequestCollection",
            "office365.directory.identitygovernance.workflow.workflow:Workflow",
        ),
    ),
    (
        "Purview's data-security plane arrives inside several suites, and the scope a content processing "
        "request computes over is the same purchase.",
        (
            "office365.directory.identitygovernance.user_data_security_and_governance:UserDataSecurityAndGovernance",
            "office365.directory.identitygovernance.user_protection_scope_container:UserProtectionScopeContainer",
        ),
    ),
    (
        "Cloud sync is sold with Entra ID P1 and directory provisioning is free; one API serves both, so "
        "the P1 claim would refuse the half that needs nothing.",
        (
            "office365.directory.synchronization.definition:DirectoryDefinition",
            "office365.directory.synchronization.job:SynchronizationJob",
            "office365.directory.synchronization.schema:SynchronizationSchema",
            "office365.directory.synchronization.synchronization:Synchronization",
        ),
    ),
    (
        "Reading the built-in role definitions is free and creating a custom role is P1. The split is per "
        "member, and a stamp on the type would over-claim the free half.",
        ("office365.directory.rolemanagement.unifiedrole.definition:UnifiedRoleDefinition",),
    ),
    (
        "Defender threat assessment is an add-on that is also inside E5, and the backup policy base is "
        "filed here too but belongs to the backup product below; one name is wrong for the other.",
        (
            "office365.directory.protection.information:InformationProtection",
            "office365.directory.protection.policy.base:ProtectionPolicyBase",
            "office365.directory.protection.rules.base:ProtectionRuleBase",
        ),
    ),
    (
        "eDiscovery is bought as PURVIEW_DISCOVERY, as COMMUNICATIONS_COMPLIANCE, or inside an E5 seat; one "
        "name on the type refuses the other two buyers.",
        (
            "office365.security.ediscovery.case_settings:EdiscoveryCaseSettings",
            "office365.security.ediscovery.custodian:EdiscoveryCustodian",
            "office365.security.ediscovery.noncustodial_data_source:EdiscoveryNoncustodialDataSource",
            "office365.security.ediscovery.review_set:EdiscoveryReviewSet",
            "office365.security.ediscovery.review_set_query:EdiscoveryReviewSetQuery",
            "office365.security.ediscovery.search:EdiscoverySearch",
        ),
    ),
    (
        "Retention is bought as RECORDS_MANAGEMENT or inside an E5 seat, the same shape as eDiscovery.",
        ("office365.security.labels.retention.collection:RetentionLabelCollection",),
    ),
    (
        "Microsoft 365 Backup is switched on per workload and no tenant here reports what it is called; the "
        "service's own refusal is a better answer than a guessed name.",
        (
            "office365.backuprestore.browse_session_base:BrowseSessionBase",
            "office365.backuprestore.protection_unit_base:ProtectionUnitBase",
            "office365.backuprestore.reports.report:BackupReport",
            "office365.backuprestore.restorepoints.collection:RestorePointCollection",
            "office365.backuprestore.restoresessions.base:RestoreSessionBase",
            "office365.backuprestore.root:BackupRestoreRoot",
            "office365.backuprestore.serviceapps.service_app:ServiceApp",
        ),
    ),
)

#: Trees whose children are separate purchases, so a family is ``directory.synchronization`` and
#: not ``directory``.
SUBDIVIDED: frozenset[str] = frozenset({"directory", "security"})


def test_every_requesting_method_names_the_permission_it_needs():
    assert LIBRARY.debt() == PENDING, "declare the permission on the method, or record the new count"


def _area(module: str) -> str:
    """The family a module belongs to: the product, or the area a subdivided tree buys separately."""
    parts = module.split(".")[1:]
    if not parts:
        return ""
    return ".".join(parts[:2]) if parts[0] in SUBDIVIDED else parts[0]


def _declaring_type(operation) -> type | None:
    """The class an operation was declared on, resolved the way an importer would."""
    found = importlib.import_module(operation.module)
    for part in operation.owner.split("."):
        found = getattr(found, part, None)
        if found is None:
            return None
    return found


def _owners_without_a_licence() -> set[str]:
    """Declaring types in a paid family that name no plan, as ``module:Type``."""
    found: set[str] = set()
    for operation in LIBRARY.declared():
        if not operation.owner or _area(operation.module) not in PAID:
            continue
        declaring = _declaring_type(operation)
        if declaring is None or licence_of(declaring) is None:
            found.add(f"{operation.module}:{operation.owner}")
    return found


def _plan_names_in(node: ast.AST) -> list[ast.AST]:
    """The expressions a marker offers as plan names, in either spelling it accepts."""
    if not isinstance(node, ast.Call):
        return []
    spelled = getattr(node.func, "id", "")
    if spelled == "requires_license":
        return list(node.args)
    if spelled != "require_permission":
        return []
    return [
        element
        for keyword in node.keywords
        if keyword.arg == "licenses"
        for element in (getattr(keyword.value, "elts", None) or [keyword.value])
    ]


def _named_plans() -> dict[str, str]:
    """Every plan name a marker spells, mapped to the line that spells it.

    Read with :mod:`ast` rather than by importing, so a marker on a class nobody imports is still
    checked - and a name built from a variable fails instead of passing unread.
    """
    package = pathlib.Path(office365.__file__).parent
    found: dict[str, str] = {}
    for path in sorted(package.rglob("*.py")):
        source = f"office365/{path.relative_to(package).as_posix()}"
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            for name in _plan_names_in(node):
                where = f"{source}:{getattr(node, 'lineno', 0)}"
                assert isinstance(name, ast.Constant) and isinstance(name.value, str), (
                    f"{where}: spell the plan name as a literal so it can be checked"
                )
                found[name.value] = where
    return found


def test_a_licence_names_a_plan_the_service_publishes():
    """A marker is checked against Microsoft's own list, not against a convention.

    The debt this closes was a SKU part number on ``SearchEntity.query``: ``SPE_E5`` is what the
    invoice calls the seat, and it matches nothing ``subscribedSkus`` reports as a plan. The
    endpoint turned out to have no licence of its own - the permissions depend on the entity types
    queried - so the claim was deleted rather than respelled.
    """
    named = _named_plans()
    assert named, "no marker names a plan: the scan is broken, not the tree"
    unknown = {name: where for name, where in named.items() if name not in SERVICE_PLANS}
    assert not unknown, f"not a published service plan name: {unknown}"


def test_a_paid_family_says_which_licence_carries_it():
    """A capability that is sold is named on the type that carries it, or explained here."""
    measured = _owners_without_a_licence()
    recorded = {owner for _reason, owners in SILENT for owner in owners}
    assert measured == recorded, "stamp the type with @requires_license, or record here why its plan cannot be named"


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
