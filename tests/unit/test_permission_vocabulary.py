"""What the tree declares, and whether it says it at all.

A live run cannot answer these: a declaration that is missing fails nothing, because a call
without a declared permission is simply a call, and the grant it silently relied on looks like
an unused one. A walk of the package is the only thing that sees either.

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

import office365
from office365.capabilities import capabilities_of
from office365.communications.callrecords.collection import CallRecordCollection
from office365.outlook.mail.messages.message import Message
from office365.permissions import index, require_permission
from office365.permissions.declaration import licence_of

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
