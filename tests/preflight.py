"""What the live suites need from a tenant, and what this one is missing.

The offline gate runs with no tenant at all, so every credentialed suite is skipped with
nothing to say what it would have needed. This module reads the requirements the tests
declare and, with ``--verify``, resolves them against the signed-in app and user - before a
test run rather than during one.

    python -m tests.preflight                 # what is blocking the most tests
    python -m tests.preflight --verify        # ... and what this tenant grants
    python -m tests.preflight --all           # every requirement, not just the blocked ones
    python -m tests.preflight --markdown      # the per-suite matrix
    python -m tests.preflight --report rpt/   # rpt/preflight.md + rpt/preflight.json
    python -m tests.preflight --grant         # grant the missing ones to the configured app

The matrix is derived from the decorators stamped by :mod:`tests.decorators`; no list of
scopes lives in this file to fall out of date.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from inspect import getmembers, isfunction
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest import TestCase

from office365.directory.rolemanagement.roles.role import DirectoryRole
from office365.graph_client import GraphClient
from office365.permissions import FLOWS as PERMISSION_FLOWS
from office365.permissions import ResourceName, catalog
from office365.runtime.client_request_exception import ClientRequestException

from tests.capabilities import (
    Needs,
    Requirement,
    TenantState,
    declared_calls,
    declared_requirement,
    forget_cached_tenant_facts,
)
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase
from tests.settings import FLOWS, Settings, settings
from tests.sharepoint.sharepoint_case import SPTestCase

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent

# The flow a test class runs under - the same mapping `tests/conftest.py` skips on.
# `GraphApplicationTestCase` subclasses `GraphDelegatedTestCase`, so it is checked first.
_FLOW_OF_BASE = (
    (GraphApplicationTestCase, "app-only"),
    (GraphDelegatedTestCase, "delegated-ropc"),
    (SPTestCase, "app-only-cert"),
)


def flow_of(test_class: type) -> str | None:
    """The flow a live test class needs, or ``None`` for an offline test."""
    return next((flow for base, flow in _FLOW_OF_BASE if issubclass(test_class, base)), None)


def needs_of(path: Path, module: ModuleType) -> Needs | None:
    """The requirements the live test classes in ``module`` declare.

    Tests are counted as pytest collects them, test *methods*, because ``dir()`` would also
    hand back a ``@property def test_site(self)`` - and a suite that claims 15 tests when
    pytest runs 13 is a report nobody trusts.
    """
    needs: Needs | None = None
    for name, obj in vars(module).items():
        if not (isinstance(obj, type) and issubclass(obj, TestCase) and obj.__module__ == module.__name__):
            continue
        flow = flow_of(obj)
        if flow is None:
            continue
        tests = [attr for attr, member in getmembers(obj, isfunction) if attr.startswith("test")]
        if needs is None:
            needs = Needs(suite=path.relative_to(ROOT).as_posix(), flow=flow)
        needs.tests += len(tests)
        for test in tests:
            requirement = declared_requirement(getattr(obj, test))
            if requirement is not None:
                needs.add(requirement, f"{name}.{test}", declared_calls(getattr(obj, test)))
    return needs


def suites(root: Path = TESTS) -> list[Needs]:
    """Every live suite under ``root`` and what it declares, by path."""
    found: list[Needs] = []
    for path in sorted(root.rglob("test_*.py")):
        module = importlib.import_module(".".join(path.relative_to(ROOT).with_suffix("").parts))
        needs = needs_of(path, module)
        if needs is not None:
            found.append(needs)
    return found


def _client(flow: str, cfg: Settings = settings) -> GraphClient | None:
    """A signed-in client for ``flow``, or ``None`` when that flow is not configured here."""
    if not cfg.is_ready(flow):
        return None
    client = GraphClient(tenant=cfg.tenant)
    if flow == "delegated-ropc":
        return client.with_username_and_password(cfg.client_id, cfg.username, cfg.password)
    if flow == "app-only":
        return client.with_client_secret(cfg.client_id, cfg.client_secret)
    if flow == "app-only-cert":
        # A certificate is an app credential like any other, and the grants to check belong
        # to the app that presents it - so the report signs in as that app.
        return client.with_certificate(cfg.client_id, cfg.cert_thumbprint, Path(cfg.cert_path).read_text())
    return None


def verify(found: list[Needs], client_id: str, cfg: Settings = settings) -> dict[Requirement, TenantState]:
    """Resolve every declared requirement against ``cfg``'s tenant, once per requirement.

    A flow that cannot sign in marks its requirements ``unverifiable`` instead of raising:
    one bad flow must not cost the report its other answers.
    """
    states: dict[Requirement, TenantState] = {}
    for flow in sorted({needs.flow for needs in found}):
        required = {requirement for needs in found if needs.flow == flow for requirement in needs.requirements}
        try:
            client = _client(flow, cfg)
            if client is None:
                continue
            states.update({requirement: TenantState.of(client, client_id, requirement) for requirement in required})
        except Exception as error:  # noqa: BLE001 - a report must survive one bad flow, not die on it
            states.update(dict.fromkeys(required, TenantState(unverifiable=f"signing in failed: {error}")))
    return states


#: The requirement label a directory role carries, as ``Requirement.groups`` spells it.
ROLE = "directory role"

#: What a refused role assignment needs. Writing to ``directoryRoles`` is one of the few
#: directory operations ``Directory.ReadWrite.All`` does not cover: it takes
#: ``RoleManagement.ReadWrite.Directory``, which this app was never consented for.
_ROLE_HINT = (
    "(assigning a directory role needs RoleManagement.ReadWrite.Directory; the Entra portal assigns one without it)"
)

#: How long to wait for a role activated a moment ago to appear in the listing.
_ROLE_READ_ATTEMPTS = 3
_ROLE_READ_PAUSE = 1.0

#: The kinds a plan can name but not grant: a licence is bought, not assigned, and this tool
#: has no business choosing who pays for it. A directory role *is* granted - to the test user.
_MANUAL_HINT = {"license": "buy seats, or assign an existing SKU to the test user"}


@dataclass(frozen=True)
class Grant:
    """One flow's names on the API that defines them - a grant does not transfer across APIs."""

    flow: str
    resource: str
    names: tuple[str, ...]

    @property
    def grantable(self) -> bool:
        """Whether this tool can write it: a permission is granted, a role assigned."""
        return self.flow in PERMISSION_FLOWS or self.flow == ROLE

    def label(self) -> str:
        """The group's label, naming the resource when it is not the default one."""
        return self.flow if str(self.resource) == str(ResourceName.Graph) else f"{self.flow} on {self.resource}"

    def __str__(self) -> str:
        return f"{self.label()}: {', '.join(self.names)}"


def _published(names: tuple[str, ...], flow: str, resource: str) -> tuple[str, ...]:
    """The names the API itself publishes, in the order given.

    The tenant records whatever string it is handed, but the token is minted from the names
    the API publishes - so a name that is not among them is consented in the directory and
    absent from every token. Asking for one is a plan that cannot succeed.
    """
    snapshot = catalog(resource)
    if snapshot is None or flow not in PERMISSION_FLOWS:
        return names
    return tuple(name for name in names if snapshot.publishes(name, flow))


def grant_plan(found: list[Needs], states: dict[Requirement, TenantState]) -> list[Grant]:
    """The smallest set of permissions that would unblock the suites, group by group.

    Every group is an any-of, so granting *one* of its names is enough; a name that appears
    in several groups is asked for once, and names on different APIs are never merged. Groups
    this tool cannot grant are still returned - the caller decides what to do with them, and
    silence would be a lie. Within a group a published name is preferred, and only when every
    name is unpublished does the plan keep one, so the group stays visible.
    """
    by_group: dict[tuple[str, str], list[tuple[str, ...]]] = {}
    for needs in found:
        for requirement, _ in needs.unmet_for(states):
            for label, names in requirement.shortfall(states[requirement]):
                by_group.setdefault((label, str(requirement.resource)), []).append(names)
    plan: list[Grant] = []
    for (label, resource), groups in by_group.items():
        remaining = list(groups)
        chosen: list[str] = []
        offered = tuple({name for group in groups for name in group})
        preferred = set(_published(offered, label, resource))
        while remaining:
            counts: dict[str, int] = {}
            for group in remaining:
                for name in group:
                    counts[name] = counts.get(name, 0) + 1
            candidates = {name: count for name, count in counts.items() if name in preferred} or counts
            # ``max`` keeps the first of equal candidates in iteration order, which is
            # declaration order - so a tie is broken by what the suites named first, not by
            # the alphabet. All three compliance roles cover these tests; the first named is
            # the narrowest one the suite itself asked for.
            best = max(candidates, key=candidates.__getitem__)
            chosen.append(best)
            remaining = [group for group in remaining if best not in group]
        plan.append(Grant(flow=label, resource=resource, names=tuple(chosen)))
    return plan


def _admin_client() -> GraphClient:
    """A signed-in administrator: a grant is a tenant-wide change and a person owns it."""
    client = GraphClient(tenant=settings.tenant).with_device_flow(settings.client_id)
    try:
        client.require_role("Global Administrator", "Privileged Role Administrator")
    except SystemExit:
        print("  (continuing; the admin role could not be verified)")
    return client


def apply_plan(client: GraphClient, plan: list[Grant], app_id: str, upn: str = "") -> tuple[list[str], list[str]]:
    """Grant what ``plan`` asks for; return (done, failed) as lines a person reads.

    A grant whose state cannot be read is attempted anyway, because applying one is
    idempotent and a missing read scope must not become a missing grant. A name the API does
    not publish is reported and not attempted. A directory role goes to ``upn``.
    """
    checks = {"delegated": client.has_delegated_permission, "application": client.has_application_permissions}
    grants = {"delegated": client.grant_delegated_permissions, "application": client.grant_application_permissions}
    done: list[str] = []
    failed: list[str] = []
    for grant in plan:
        if not grant.grantable:
            continue
        for name in grant.names:
            entry = f"{grant.label()} {name}"
            if grant.flow == ROLE:
                held, reason = _grant_role(client, name, upn)
                (done if held else failed).append(entry if held else f"{entry}: {reason} {_ROLE_HINT}")
                continue
            if not _published((name,), grant.flow, grant.resource):
                failed.append(f"{entry}: {grant.resource} does not publish this name")
                continue
            try:
                already = checks[grant.flow](name, app_id, resource=grant.resource)
            except (ClientRequestException, KeyError):
                already = False
            if already:
                done.append(f"{entry} (already granted)")
                continue
            try:
                grants[grant.flow](app_id, name, resource=grant.resource).execute_query()
            except (ClientRequestException, KeyError) as exc:
                failed.append(f"{entry}: {_first_line(exc)}")
                continue
            done.append(entry)
    return done, failed


def _grant_role(client: GraphClient, name: str, upn: str) -> tuple[bool, str]:
    """Assign a directory role to ``upn``; (held afterwards, why it is not).

    ``directoryRoles`` lists only the roles the tenant has *activated*, so one nobody has
    ever held has no members collection to add to; activating first makes the two steps one
    operation. Activation is a write and can be refused, and the reason is the answer.
    """
    refused = ""
    role = _active_role(client, name)
    if role is None:
        try:
            client.directory_roles.assign(name).execute_query()
        except ClientRequestException as exc:
            refused = _first_line(exc)
        role = _active_role(client, name)
    if role is None:
        return False, refused or f"the directory lists no role named {name!r}"
    try:
        role.add_member(upn).execute_query()
    except ClientRequestException as exc:
        return False, _first_line(exc)
    held = role.members.get().execute_query()
    if any(member.get_property("userPrincipalName") == upn for member in held):
        return True, ""
    return False, f"{upn} was not a member after the assignment"


def _active_role(client: GraphClient, name: str) -> DirectoryRole | None:
    """The activated role ``name``, waiting out the lag between activating one and listing it."""
    for attempt in range(_ROLE_READ_ATTEMPTS):
        if attempt:
            time.sleep(_ROLE_READ_PAUSE)
        found = next((role for role in client.directory_roles.get().execute_query() if role.display_name == name), None)
        if found is not None:
            return found
    return None


def _first_line(exc: Exception) -> str:
    """The first line of a server message - the rest is advice that names no name."""
    return str(exc).splitlines()[0] or exc.__class__.__name__


def grant_missing(found: list[Needs], *, yes: bool = False) -> int:
    """Read what the suites need, grant what is missing, then read the tenant again."""
    states = verify(found, settings.client_id)
    if not states:
        print("Nothing was verified: no auth flow is ready yet - fill .env from .env.example first.")
        return 1
    plan = grant_plan(found, states)
    if not plan:
        print(f"Every declared permission is already granted to {settings.client_id}.")
        return 0
    print(f"\nPermissions the live suites declare and {settings.client_id} lacks:")
    for grant in plan:
        hint = "" if grant.grantable else f" ({_MANUAL_HINT.get(grant.flow, 'configure it by hand')})"
        print(f"  {grant}{hint}")
    if not yes and input(f"Grant these to {settings.client_id} now? [y/N]: ").strip().lower() not in ("y", "yes"):
        print("Nothing granted.")
        return 0

    done, failed = apply_plan(_admin_client(), plan, settings.client_id, settings.username)
    print("\n".join([f"  granted: {line}" for line in done] + [f"  failed:  {line}" for line in failed]))
    forget_cached_tenant_facts()
    remaining = grant_plan(found, verify(found, settings.client_id))
    if remaining:
        print("\nStill missing:")
        print("\n".join(f"  {grant}" for grant in remaining))
        print("Re-run `python -m tests.preflight --verify` once the rest is in place.")
        return 1
    print("\nEvery declared permission is now granted. `python -m tests.preflight --verify` will confirm it.")
    return 1 if failed else 0


@dataclass(frozen=True)
class Row:
    """One declared requirement: what unblocks it, what this tenant answers, and what it came from.

    ``calls`` is the provenance - the model methods the declaring tests exercise - so a row
    says not only how many tests a grant unblocks but what in the library asks for it.
    """

    requirement: Requirement
    flow: str
    tests: int
    facts: TenantState | None
    calls: tuple[str, ...] = ()

    @property
    def state(self) -> str:
        """One of ``met``, ``missing``, ``unverified`` - the only three answers there are."""
        if self.facts is None or self.facts.unverifiable:
            return "unverified"
        return "met" if self.requirement.satisfied_by(self.facts) else "missing"

    @property
    def needs(self) -> str:
        """The delta - the groups this tenant leaves unmet - or the whole rule when there is no answer."""
        if self.facts is None:
            return self.requirement.describe()
        needs = " and ".join(self.requirement.unmet(self.facts)) or "met"
        roles = self.requirement.bypass_roles
        # A bypass role is an alternative to everything above it, so it is worth naming
        # until the row is satisfied on its own terms.
        return f"{needs} (or {', '.join(roles)})" if roles and self.state != "met" else needs

    def __str__(self) -> str:
        # A met row has no delta, so it prints the rule it satisfies instead of the word.
        return f"{self.tests:>4}  {self.requirement.describe() if self.state == 'met' else self.needs}"

    def json(self) -> dict[str, Any]:
        return {
            "requirement": self.requirement.describe(),
            "flow": self.flow,
            "tests": self.tests,
            "state": self.state,
            "needs": self.needs,
            "calls": list(self.calls),
        }


class Report:
    """One measurement of the tree and the tenant, in three renderings.

    ``found`` is what the suites declare; ``states`` is what this tenant answered, and is
    empty when nothing was verified. The rows are the whole report - the terminal view prints
    the ones that need something, the file prints all of them, and a tool gets them as JSON.
    """

    #: How many rows a screen shows: a person reads the ones that unblock the most tests.
    SHOWN = 10

    def __init__(self, found: list[Needs], states: dict[Requirement, TenantState]):
        self.found = found
        self.states = states
        self.tenant = settings.tenant
        self.flows = {flow: settings.missing_for(flow) for flow in FLOWS}
        self.suites = len(found)
        self.tests = sum(needs.tests for needs in found)
        tests: dict[Requirement, list[str]] = {}
        calls: dict[Requirement, list[str]] = {}
        for needs in found:
            for requirement, declared in needs.requirements.items():
                tests.setdefault(requirement, []).extend(declared)
                known = calls.setdefault(requirement, [])
                known.extend(call for call in needs.calls.get(requirement, ()) if call not in known)
        self.rows = [
            Row(
                requirement,
                requirement.label("delegated" if requirement.delegated else "application"),
                len(tests[requirement]),
                states.get(requirement),
                tuple(sorted(calls[requirement])),
            )
            for requirement in sorted(tests, key=lambda item: (-len(tests[item]), item.describe()))
        ]

    @property
    def blocking(self) -> list[Row]:
        """The requirements that need something, in the order they are worth fixing."""
        return [row for row in self.rows if row.state != "met"]

    def text(self, *, show_all: bool = False) -> str:
        """The terminal view: the counts, the flows that are not ready, and the delta."""
        lines = [
            f"Live-test preflight - {self.tenant or 'no tenant configured'}",
            f"{self.suites} suites, {self.tests} tests, {sum(len(needs.requirements) for needs in self.found)}"
            f" requirements ({len(self.rows)} distinct)",
            "",
            "Flows",
        ]
        missing = {flow: gaps for flow, gaps in self.flows.items() if gaps}
        if missing:
            lines += [f"  {flow}: missing {', '.join(gaps)}" for flow, gaps in missing.items()]
        else:
            lines.append(f"  all {len(self.flows)} configured")
        counts = {word: [row for row in self.rows if row.state == word] for word in ("met", "missing", "unverified")}
        summary = ", ".join(f"{len(rows)} {word}" for word, rows in counts.items() if rows) or "none declared"
        lines += ["", f"Requirements   {summary}"]
        if not self.states:
            lines.append("  not verified: --verify resolves them against this tenant")
        shown = self.rows if show_all else self.blocking[: self.SHOWN]
        lines += [f"  {row}" for row in shown]
        hidden = len(self.blocking) - len(shown)
        if hidden > 0:
            lines.append(f"  ... {hidden} more; --all lists every requirement")
        if self.states and not self.blocking:
            lines.append("  every declared requirement is met")
        return "\n".join(lines) + "\n"

    def markdown(self) -> str:
        """The report: what every live suite needs, and what this environment answers."""
        lines = [
            "# Live-test preflight",
            "",
            f"Generated by `python -m tests.preflight` for tenant `{self.tenant or '<none>'}`.",
            "",
            "## Auth flows",
            "",
            "| flow | state |",
            "| --- | --- |",
        ]
        for flow, gaps in self.flows.items():
            state = f"not configured: {', '.join(gaps)}" if gaps else "ok"
            lines.append(f"| {FLOWS[flow].label} (`{flow}`) | {state} |")
        rows = {row.requirement: row for row in self.rows}
        lines += [
            "",
            f"{self.suites} live suites, {self.tests} live tests, {len(self.rows)} declared permission requirements.",
            "",
            "`via` names the model methods each test derived its requirement from; a requirement",
            "stated by hand with `@requires_delegated`/`@requires_application` is a `-`.",
            "",
            "| suite | flow | tests | declared | via | status |",
            "| --- | --- | ---: | --- | --- | --- |",
        ]
        for needs in self.found:
            if not needs.requirements:
                lines.append(
                    f"| `{needs.suite}` | `{needs.flow}` | {needs.tests} | none declared | - | credentials only |"
                )
            for requirement in sorted(needs.requirements, key=Requirement.describe):
                row = rows[requirement]
                calls = ", ".join(call.rpartition(":")[2] for call in needs.calls.get(requirement, ())) or "-"
                lines.append(
                    f"| `{needs.suite}` | `{needs.flow}` | {len(needs.requirements[requirement])} |"
                    f" {requirement.describe()} | {calls} | {row.state} |"
                )
        lines += ["", "## Missing", ""]
        if not self.states:
            lines.append("Not verified: run with `--verify` (needs credentials) to resolve these against the tenant.")
        elif not self.blocking:
            lines.append("Every declared requirement is met.")
        else:
            lines += [f"- {str(row).strip()}" for row in self.blocking]
        return "\n".join(lines) + "\n"

    def json(self) -> str:
        """The same report for CI: flows, and every requirement with its state."""
        payload = {
            "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "tenant": self.tenant,
            "flows": {flow: {"label": FLOWS[flow].label, "missing": gaps} for flow, gaps in self.flows.items()},
            "rows": [row.json() for row in self.rows],
        }
        return json.dumps(payload, indent=2) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report what the live test suites need from a tenant.")
    parser.add_argument("--verify", action="store_true", help="resolve the requirements against the signed-in tenant")
    parser.add_argument("--all", action="store_true", help="list every requirement, not just the ones needing action")
    parser.add_argument("--markdown", action="store_true", help="print the per-suite report instead of the summary")
    parser.add_argument("--report", metavar="DIR", help="write preflight.md into DIR (a report for people)")
    parser.add_argument("--json", metavar="DIR", help="write preflight.json into DIR (a report for tools)")
    parser.add_argument("--strict", action="store_true", help="exit 1 when a flow or requirement is not satisfied")
    parser.add_argument("--grant", action="store_true", help="grant the missing permissions to the app (asks first)")
    parser.add_argument("-y", "--yes", action="store_true", help="do not ask before --grant")
    args = parser.parse_args(argv)

    found = suites()
    if args.grant:
        return grant_missing(found, yes=args.yes)
    # --strict cannot mean anything without an answer to compare against, so it verifies too.
    states = verify(found, settings.client_id) if (args.verify or args.strict) else {}
    report = Report(found, states)
    if not (args.report or args.json):
        sys.stdout.write(report.markdown() if args.markdown else report.text(show_all=args.all))
    artifacts = ((args.report, report.markdown, "preflight.md"), (args.json, report.json, "preflight.json"))
    for directory, render, name in artifacts:
        if not directory:
            continue
        path = Path(directory) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(), encoding="utf-8")
        print(f"Wrote {path}")
    if not args.strict:
        return 0
    unconfigured = [flow for flow in FLOWS if settings.missing_for(flow)]
    unmet = [row for row in report.rows if row.state != "met" and row.facts is not None]
    return 1 if unconfigured or unmet else 0


if __name__ == "__main__":
    raise SystemExit(main())
