"""Routing and the tree must name the same home for a type.

``type_routing`` decides where a *new* type is rendered; ``--place`` decides where an
*existing* one belongs.  The two are written by different passes, so they drift silently:
a catch-all like ``Device*`` keeps generating into a directory the tree has since
outgrown, and the mistake only shows up when the next type lands in the wrong product.
These tests read the tree and the rules together and ask one question of each type --
does the rule point at the directory the file is in? -- so a catch-all that starts
swallowing another product's types fails here instead of in a review.

The rules are read, not applied: the check is agreement, and the direction (rule
grows more specific, or the file moves) stays a human decision.
"""

from __future__ import annotations

import ast
import re

from generator.cli.session import GENERATOR_DIR, Session
from generator.planning.routing import Router

_ROOT = GENERATOR_DIR.parent
_PACKAGE = _ROOT / "office365"
_TYPE_NAME = re.compile(r'return\s+"(microsoft\.graph\.[^"]+)"')


def _router() -> Router:
    return Router.from_options(Session.open("graph").options.builder_context())


def _typed_classes() -> list[tuple[str, str, str]]:
    """``(class name, OData type name, package)`` for every class that declares a type.

    Read from the source rather than from the registry: the question is about the tree
    as committed, which is what a reader sees, not about what the last render knew.
    """
    found: list[tuple[str, str, str]] = []
    for path in sorted(_PACKAGE.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "entity_type_name" not in source:
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        package = "office365." + ".".join(path.relative_to(_PACKAGE).parts[:-1])
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            match = None
            for sub in ast.walk(node):
                if isinstance(sub, ast.Return) and isinstance(sub.value, ast.Constant):
                    if isinstance(sub.value.value, str):
                        match = _TYPE_NAME.search(f'return "{sub.value.value}"')
                        if match:
                            break
            if match:
                found.append((node.name, match.group(1), package))
    return found


def _inside(package: str, family: str) -> bool:
    return package == family or package.startswith(family + ".")


def _agrees(package: str, routed: str) -> bool:
    """One is an ancestor of the other: the file may not have moved *down* yet."""
    return _inside(routed, package) or _inside(package, routed)


def test_every_intune_type_routes_into_the_intune_tree() -> None:
    """A rule may not send an Intune type to another product, nor name a distant home."""
    router = _router()

    disagreements = [
        f"{name:38} {package:58} -> {routed}"
        for name, odata, package in _typed_classes()
        if _inside(package, "office365.intune")
        for routed in [router.module_for(odata, allow_fallback=False)]
        if routed and not (_inside(routed, "office365.intune") and _agrees(package, routed))
    ]

    assert disagreements == [], "\n".join(disagreements)


def test_no_type_outside_intune_routes_into_it() -> None:
    """The Intune adjectives used to swallow Entra types; the narrowed rules must not."""
    router = _router()

    intrusions = [
        f"{name:38} {package:58} -> {routed}"
        for name, odata, package in _typed_classes()
        if not _inside(package, "office365.intune")
        for routed in [router.module_for(odata, allow_fallback=False)]
        if routed and _inside(routed, "office365.intune")
    ]

    assert intrusions == [], "\n".join(intrusions)


def test_a_narrower_prefix_beats_the_wider_one() -> None:
    """``CloudPc*`` has to outrun ``Cloud*`` for the cloud PC family to stay together."""
    router = _router()

    assert router.module_for("microsoft.graph.CloudPcAuditEvent") == (
        "office365.intune.devices.management.virtualendpoint.cloudpcs"
    )
    assert router.module_for("microsoft.graph.CloudPcProvisioningPolicy") == (
        "office365.intune.devices.management.virtualendpoint.cloudpcs"
    )
    assert router.module_for("microsoft.graph.CloudAppSecurityState") == "office365.security"


def test_print_usage_is_a_report_not_a_printer() -> None:
    """The usage rows are reports about the print service; only the printers are printers.

    ``Print*`` names the family root, not a leaf: the connector, the service and the task
    live in their own subpackages, which the placement descent reaches from the type name.
    """
    router = _router()

    assert router.module_for("microsoft.graph.PrintUsageByPrinter") == "office365.reports"
    assert router.module_for("microsoft.graph.PrinterShare") == "office365.intune.print.shares"
    assert router.module_for("microsoft.graph.Printer") == "office365.intune.print.printers"
    assert router.module_for("microsoft.graph.PrintConnector") == "office365.intune.print"
    assert router.module_for("microsoft.graph.PrintService") == "office365.intune.print"


def _unified() -> list[tuple[str, str, str]]:
    """``(class name, OData type name, package)`` for every ``Unified*`` type in the tree."""
    return [row for row in _typed_classes() if row[1].rsplit(".", 1)[-1].lower().startswith("unified")]


def test_a_unified_type_keeps_the_root_that_reaches_it() -> None:
    """PIM is three getters, not one prefix.

    ``Unified*`` put the role schedules, the role policies and three unrelated types in
    one directory. Every rule now names the getter that reads the type, so a type that
    lives in ``office365.directory`` has to route back into it.
    """
    router = _router()

    disagreements = [
        f"{name:52} {package:64} -> {routed}"
        for name, odata, package in _unified()
        if _inside(package, "office365.directory")
        for routed in [router.module_for(odata, allow_fallback=False)]
        if not (routed and _inside(routed, "office365.directory") and _agrees(package, routed))
    ]

    assert disagreements == [], "\n".join(disagreements)


def test_no_unified_type_outside_the_directory_tree_routes_into_it() -> None:
    """The group and simulation records read as Entra types; they are security records."""
    router = _router()

    intrusions = [
        f"{name:52} {package:64} -> {routed}"
        for name, odata, package in _unified()
        if not _inside(package, "office365.directory")
        for routed in [router.module_for(odata, allow_fallback=False)]
        if routed and _inside(routed, "office365.directory")
    ]

    assert intrusions == [], "\n".join(intrusions)


def test_the_role_family_follows_its_two_getters() -> None:
    """``rbacApplication`` reaches the schedules; ``/policies`` reaches the policies."""
    router = _router()

    assert router.module_for("microsoft.graph.UnifiedRoleAssignmentSchedule") == (
        "office365.directory.rolemanagement.unifiedrole"
    )
    assert router.module_for("microsoft.graph.UnifiedRbacResourceNamespace") == (
        "office365.directory.rolemanagement.unifiedrole"
    )
    assert router.module_for("microsoft.graph.UnifiedRoleManagementPolicyRule") == (
        "office365.directory.policies.unifiedrolemanagement"
    )
    assert router.module_for("microsoft.graph.UnifiedApprovalStage") == "office365.directory"
    assert router.module_for("microsoft.graph.UnifiedStorageQuota") == "office365.directory.users"
