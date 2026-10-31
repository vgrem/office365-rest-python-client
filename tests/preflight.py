"""What the live suites need from a tenant, and what this one is missing.

The offline gate runs with no tenant at all, so every credentialed suite is skipped
with nothing to say what it would have needed. This module makes that known
*before* a test run: it reads the requirements the tests declare, groups them by
suite and by auth flow, and — with ``--verify`` — resolves them against the signed-in
app and user.

    python -m tests.preflight                 # what is blocking the most tests
    python -m tests.preflight --verify        # ... and what this tenant grants
    python -m tests.preflight --all           # every requirement, not just the blocked ones
    python -m tests.preflight --markdown      # the per-suite matrix
    python -m tests.preflight --report rpt/   # rpt/preflight.md + rpt/preflight.json

The matrix is derived from the decorators stamped by :mod:`tests.decorators`; there is
no list of scopes anywhere in this file to fall out of date.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import textwrap
from dataclasses import dataclass
from datetime import datetime, timezone
from inspect import getmembers, isfunction
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest import TestCase

from office365.graph_client import GraphClient
from office365.permissions import FLOWS as PERMISSION_FLOWS
from office365.permissions import ResourceName

from tests.capabilities import Needs, Requirement, TenantState, declared_requirement
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase
from tests.settings import FLOWS, Settings, settings
from tests.sharepoint.sharepoint_case import SPTestCase

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent

#: The auth flow a test class runs under — the same mapping `tests/conftest.py` skips on.
#: ``GraphApplicationTestCase`` subclasses ``GraphDelegatedTestCase``, so it is checked first.
_FLOW_OF_BASE = (
    (GraphApplicationTestCase, "app-only"),
    (GraphDelegatedTestCase, "delegated-ropc"),
    (SPTestCase, "app-only-cert"),
)


def flow_of(test_class: type) -> str | None:
    """The auth flow a live test class needs, or ``None`` when it is an offline test."""
    for base, flow in _FLOW_OF_BASE:
        if issubclass(test_class, base):
            return flow
    return None


def _module_name(path: Path) -> str:
    return ".".join(path.relative_to(ROOT).with_suffix("").parts)


def _import(path: Path) -> ModuleType:
    return importlib.import_module(_module_name(path))


def _ordered(requirement: Requirement) -> tuple[str, ...]:
    """A stable sort key: the widest group first, then alphabetical."""
    return tuple(f"{label}:{','.join(names)}" for label, names, _ in requirement.groups())


def needs_of(path: Path, module: ModuleType) -> Needs | None:
    """The requirements the test classes defined in ``module`` declare."""
    needs: Needs | None = None
    for name, obj in vars(module).items():
        if not (isinstance(obj, type) and issubclass(obj, TestCase) and obj.__module__ == module.__name__):
            continue
        flow = flow_of(obj)
        if flow is None:
            continue
        # Count what pytest collects -- test *methods*, in a class pytest would collect.
        # ``dir()`` would also hand back a ``@property def test_site(self)``, and a
        # suite that says it has 15 tests when pytest runs 13 is a report nobody trusts.
        test_names = [attr for attr, member in getmembers(obj, isfunction) if attr.startswith("test")]
        if needs is None:
            needs = Needs(suite=path.relative_to(ROOT).as_posix(), flow=flow)
        needs.tests += len(test_names)
        for test_name in test_names:
            requirement = declared_requirement(getattr(obj, test_name))
            if requirement is not None:
                needs.add(requirement, f"{name}.{test_name}")
    return needs


def suites(root: Path = TESTS) -> list[Needs]:
    """Every live suite under ``root`` and what it declares, sorted by path."""
    found: list[Needs] = []
    for path in sorted(root.rglob("test_*.py")):
        needs = needs_of(path, _import(path))
        if needs is not None:
            found.append(needs)
    return found


def _client(flow: str, cfg: Settings = settings) -> GraphClient | None:
    """A signed-in Graph client for ``flow``, or ``None`` when it cannot be built here."""
    if not cfg.is_ready(flow):
        return None
    client = GraphClient(tenant=cfg.tenant)
    if flow == "delegated-ropc":
        return client.with_username_and_password(cfg.client_id, cfg.username, cfg.password)
    if flow == "app-only":
        return client.with_client_secret(cfg.client_id, cfg.client_secret)
    if flow == "app-only-cert":
        # The certificate is an app credential like any other: Graph accepts it, and the grants
        # to check belong to the app that presents it, so the report must sign in as that app.
        return client.with_certificate(cfg.client_id, cfg.cert_thumbprint, Path(cfg.cert_path).read_text())
    return None


def verify(found: list[Needs], client_id: str, cfg: Settings = settings) -> dict[Requirement, TenantState]:
    """Resolve every declared requirement against the tenant, once per requirement.

    ``cfg`` is passed by the setup wizard, which has just written ``.env``: the module
    level :data:`settings` was read before that file existed.
    """
    states: dict[Requirement, TenantState] = {}
    for flow in sorted({needs.flow for needs in found}):
        required = {requirement for needs in found if needs.flow == flow for requirement in needs.requirements}
        try:
            client = _client(flow, cfg)
            if client is None:
                continue
            for requirement in required:
                states[requirement] = TenantState.of(client, client_id, requirement)
        except Exception as error:  # noqa: BLE001 - a report must survive one bad flow, not die on it
            failure = TenantState(unverifiable=f"signing in failed: {error}")
            states.update(dict.fromkeys(required, failure))
    return states


@dataclass(frozen=True)
class Grant:
    """What a person is asked to approve: one flow's names on the API that defines them.

    The resource is part of the grant and not a detail of applying it: ``Sites.FullControl.All``
    on the SharePoint service principal is a different grant from Graph's, and a wizard that
    dropped the resource would grant - or report - one under the other's name.
    """

    flow: str
    resource: str
    names: tuple[str, ...]

    @property
    def grantable(self) -> bool:
        """Whether this is a permission on the app at all - a directory role or a SKU is not."""
        return self.flow in PERMISSION_FLOWS

    def label(self) -> str:
        """The group's label, naming the resource when it is not the default one."""
        return self.flow if str(self.resource) == str(ResourceName.Graph) else f"{self.flow} on {self.resource}"


def grant_plan(found: list[Needs], states: dict[Requirement, TenantState]) -> list[Grant]:
    """The smallest set of permissions that would unblock the suites, group by group.

    Every group is an any-of, so granting *one* of its names is enough — granting all of
    them would ask for more than any test needs. A name that appears in several unmet
    groups is asked for once, and names on different APIs are never merged, because they are
    not the same grant. Groups this wizard cannot grant are still returned: the caller decides
    what to do with them, and silence would be a lie.
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
        while remaining:
            counts: dict[str, int] = {}
            for group in remaining:
                for name in group:
                    counts[name] = counts.get(name, 0) + 1
            best = max(sorted(counts), key=counts.__getitem__)
            chosen.append(best)
            remaining = [group for group in remaining if best not in group]
        plan.append(Grant(flow=label, resource=resource, names=tuple(chosen)))
    return plan


def render_plan(plan: list[Grant]) -> str:
    """The plan as a short list a person can approve, one line per group."""
    width = max([15, *(len(grant.label()) for grant in plan)])
    return "\n".join(f"  {grant.label():<{width}} {', '.join(grant.names)}" for grant in plan)


def _flow(row: _Row) -> str:
    """The column value: the flow, and the API when it is not Microsoft Graph.

    ``label()`` spells the resource out in full, which is right in a sentence and 41 columns
    wide in a table; the short name is the enum member, so no second table of names exists.
    """
    requirement = row.requirement
    flow = "delegated" if requirement.delegated else "application"
    try:
        api = ResourceName(requirement.resource).name
    except ValueError:
        return requirement.label(flow)
    return flow if api == ResourceName.Graph.name else f"{flow} ({api})"


def _article(word: str) -> str:
    """``a`` or ``an``, so the alternative reads as a sentence fragment and not a template."""
    return "an" if word[:1].lower() in "aeiou" else "a"


def _group(label: str, names: tuple[str, ...], show_all: bool) -> str:
    """One any-of group as a cell: the names, or the one name to grant and how many others."""
    if show_all:
        spelled = ", ".join(names)
    else:
        spelled = names[0] + (f" (+{len(names) - 1})" if len(names) > 1 else "")
    return spelled if label.startswith(PERMISSION_FLOWS) else f"{label}: {spelled}"


def _tests(count: int) -> str:
    """A count with its noun: ``1 test`` is a measurement, ``1 tests`` is a typo."""
    return f"{count} test" if count == 1 else f"{count} tests"


@dataclass(frozen=True)
class _Row:
    """One requirement, the tests that declared it, and what this tenant answers."""

    requirement: Requirement
    tests: tuple[str, ...]
    state: str
    facts: TenantState | None


class Report:
    """One measurement of the tree and the tenant, in three renderings.

    ``found`` is what the suites declare; ``states`` is what this tenant answered, and
    is empty when nothing was verified. The screen and the file want different things
    from the same facts: a table of 147 suites by 192 requirements is a report, not
    something to read, so the terminal view deduplicates requirements, ranks them by
    the tests they unblock, and collapses the satisfied ones to a count.
    """

    #: How many requirement lines a screen shows. The rest affect fewer tests, and a
    #: person reading this wants the ones that matter, not all 149.
    SHOWN = 10

    #: Where a long list of alternatives wraps, hanging under the column it belongs to.
    WIDTH = 120

    def __init__(self, found: list[Needs], states: dict[Requirement, TenantState]):
        self.found = found
        self.states = states
        self.tenant = settings.tenant
        self.flows = {flow: settings.missing_for(flow) for flow in FLOWS}
        self.suites = len(found)
        self.tests = sum(needs.tests for needs in found)
        self.declared = sum(len(needs.requirements) for needs in found)
        totals: dict[Requirement, list[str]] = {}
        for needs in found:
            for requirement, tests in needs.requirements.items():
                totals.setdefault(requirement, []).extend(tests)
        self.rows = [
            _Row(requirement, tuple(totals[requirement]), self.state(requirement), self.states.get(requirement))
            for requirement in sorted(totals, key=lambda item: (-len(totals[item]), item.describe()))
        ]

    def state(self, requirement: Requirement) -> str:
        """One of ``met``, ``missing``, ``unverified`` -- the only three answers there are."""
        state = self.states.get(requirement)
        if state is None or state.unverifiable:
            return "unverified"
        return "met" if requirement.satisfied_by(state) else "missing"

    def status(self, requirement: Requirement) -> str:
        """The same answer in prose, for the report a person reads about a tenant."""
        state = self.states.get(requirement)
        if state is None:
            return "not verified"
        if state.unverifiable:
            return f"not verified ({state.unverifiable})"
        unmet = requirement.unmet(state)
        return "met" if not unmet else "missing " + " and ".join(unmet)

    @property
    def counts(self) -> dict[str, int]:
        return {word: sum(1 for row in self.rows if row.state == word) for word in ("met", "missing", "unverified")}

    @property
    def blocking(self) -> list[_Row]:
        """The requirements that need something, in the order they are worth fixing."""
        return [row for row in self.rows if row.state != "met"]

    @staticmethod
    def _needs(row: _Row, show_all: bool) -> list[str]:
        """The groups this tenant leaves unmet, one string each: the delta, not the whole rule.

        A requirement is a conjunction of any-of groups, and spelling all of it hides the
        point: a row blocked on a directory role and a licence does not need its scope named
        again, because that half is already granted. Only the unmet groups are listed, and
        the flow they belong to is a column, so the name is not repeated either.

        ``--all`` spells every alternative; otherwise each group collapses to the first name
        and a count, because a line only has to say what to grant.
        """
        requirement = row.requirement
        if row.facts is None or row.state in ("met", "unverified"):
            # Nothing was left out or nothing can be: either way the whole rule is the answer,
            # and its groups still fit under the columns instead of in one 130-column sentence.
            groups = [(label, names) for label, names, _ in requirement.groups()]
        else:
            groups = requirement.shortfall(row.facts)
        return [_group(label, names, show_all) for label, names in groups] or [requirement.describe()]

    def _table(self, rows: list[_Row], show_all: bool, heading: str = "to add") -> list[str]:
        """The rows as a table: tests, the flow, and what is missing under a ``+``.

        ``+`` is the line that has to be added to the tenant, and an unprefixed line is a
        requirement already met - the two markers a diff uses, for the same reason. A role
        that satisfies a whole requirement rides at the end of its first line, where it is
        the alternative to everything listed under it.
        """
        width = max(len(_flow(row)) for row in rows)
        hanging = " " * (11 + width + 2)
        lines = [f"  {'tests':>7}  {'flow':<{width}}  {heading if self.states else 'needs'}"]
        for row in rows:
            marker = {"missing": "+ ", "unverified": "? "}.get(row.state, "")
            indent = hanging + "   " * bool(marker)
            roles = row.requirement.bypass_roles
            bypass = f"(or {_article(roles[0])} {' / '.join(roles)} role)" if roles and row.state != "met" else ""
            wrapped: list[list[str]] = []
            for index, cell in enumerate(self._needs(row, show_all)):
                lead = hanging if index else f"  {len(row.tests):>7}  {_flow(row):<{width}}  "
                wrapped.append(textwrap.wrap(f"{lead}{marker}{cell}", width=self.WIDTH, subsequent_indent=indent))
            if bypass:
                last = wrapped[0][-1]
                if len(last) + len(bypass) + 2 <= self.WIDTH:
                    wrapped[0][-1] = f"{last}  {bypass}"
                else:
                    wrapped[0].append(f"{indent}{bypass}")
            lines.extend(line for group in wrapped for line in group)
        return lines

    def text(self, *, show_all: bool = False) -> str:
        """The terminal view: the counts, the flows that are not ready, and the delta."""
        lines = [
            f"Live-test preflight - {self.tenant or 'no tenant configured'}",
            f"{self.suites} suites, {_tests(self.tests)}, {self.declared} requirements ({len(self.rows)} distinct)",
            "",
            "Flows",
        ]
        unconfigured = {flow: missing for flow, missing in self.flows.items() if missing}
        for flow, missing in unconfigured.items():
            lines.append(f"  {flow:<15} not configured (missing: {', '.join(missing)})")
        if not unconfigured:
            lines.append(f"  all {len(self.flows)} configured")
        summary = ", ".join(f"{count} {word}" for word, count in self.counts.items() if count) or "none declared"
        lines += ["", f"Requirements   {summary}"]
        if not self.states:
            lines.append("  not verified: --verify resolves them against this tenant")
        shown = self.blocking if show_all else self.blocking[: self.SHOWN]
        lines += self._table(shown, show_all)
        hidden = len(self.blocking) - len(shown)
        if hidden:
            lines.append(f"  ... {hidden} with fewer tests; --all spells every alternative")
        met = [row for row in self.rows if row.state == "met"]
        if show_all and met:
            lines += ["", f"  met ({len(met)})", *self._table(met, show_all, heading="granted")]
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
        for flow, missing in self.flows.items():
            state = f"not configured (missing: {', '.join(missing)})" if missing else "configured"
            lines.append(f"| {FLOWS[flow].label} (`{flow}`) | {state} |")

        lines += [
            "",
            f"{self.suites} live suites, {self.tests} live tests, {self.declared} declared permission requirements.",
            "",
            "## Suites",
            "",
            "| suite | flow | tests | declared | status |",
            "| --- | --- | ---: | --- | --- |",
        ]
        for needs in self.found:
            if not needs.requirements:
                lines.append(f"| `{needs.suite}` | `{needs.flow}` | {needs.tests} | none declared | credentials only |")
                continue
            for requirement in sorted(needs.requirements, key=_ordered):
                tests = len(needs.requirements[requirement])
                lines.append(
                    f"| `{needs.suite}` | `{needs.flow}` | {tests} | "
                    f"{requirement.describe()} | {self.status(requirement)} |"
                )

        lines += ["", "## Missing", ""]
        if not self.states:
            lines.append("Not verified: run with `--verify` (needs credentials) to resolve these against the tenant.")
        else:
            missing = [row for row in self.blocking]
            if not missing:
                lines.append("Every declared requirement is met.")
            for row in missing:
                lines.append(f"- {row.requirement.describe()} - {_tests(len(row.tests))}, {row.state}")
        return "\n".join(lines) + "\n"

    def json(self) -> str:
        """The same report for CI: flows, suites, requirements and their status."""
        payload: dict[str, Any] = {
            "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "tenant": self.tenant,
            "flows": {flow: {"label": FLOWS[flow].label, "missing": missing} for flow, missing in self.flows.items()},
            "suites": [
                {
                    "suite": needs.suite,
                    "flow": needs.flow,
                    "tests": needs.tests,
                    "requirements": [
                        {
                            "declared": requirement.describe(),
                            "status": self.status(requirement),
                            "tests": needs.requirements[requirement],
                        }
                        for requirement in sorted(needs.requirements, key=_ordered)
                    ],
                }
                for needs in self.found
            ],
        }
        return json.dumps(payload, indent=2) + "\n"


def _write(report_dir: Path, text: str, name: str) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / name
    path.write_text(text, encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report what the live test suites need from a tenant.")
    parser.add_argument("--verify", action="store_true", help="resolve the requirements against the signed-in tenant")
    parser.add_argument("--all", action="store_true", help="list every requirement, not just the ones needing action")
    parser.add_argument("--markdown", action="store_true", help="print the per-suite report instead of the summary")
    parser.add_argument("--report", metavar="DIR", help="write preflight.md into DIR (a report for people)")
    parser.add_argument("--json", metavar="DIR", help="write preflight.json into DIR (a report for tools)")
    parser.add_argument("--strict", action="store_true", help="exit 1 when a flow or requirement is not satisfied")
    args = parser.parse_args(argv)

    found = suites()
    # --strict cannot mean anything without an answer to compare against, so it verifies too.
    states = verify(found, settings.client_id) if (args.verify or args.strict) else {}
    report = Report(found, states)
    if not (args.report or args.json):
        sys.stdout.write(report.markdown() if args.markdown else report.text(show_all=args.all))
    if args.report:
        print(f"Wrote {_write(Path(args.report), report.markdown(), 'preflight.md')}")
    if args.json:
        print(f"Wrote {_write(Path(args.json), report.json(), 'preflight.json')}")

    if not args.strict:
        return 0
    unconfigured = [flow for flow in FLOWS if settings.missing_for(flow)]
    unmet = [
        requirement
        for needs in found
        for requirement in needs.requirements
        if (state := states.get(requirement)) is not None and not requirement.satisfied_by(state)
    ]
    return 1 if unconfigured or unmet else 0


if __name__ == "__main__":
    raise SystemExit(main())
