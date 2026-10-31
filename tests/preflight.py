"""What the live suites need from a tenant, and what this one is missing.

The offline gate runs with no tenant at all, so every credentialed suite is skipped
with nothing to say what it would have needed. This module makes that known
*before* a test run: it reads the requirements the tests declare, groups them by
suite and by auth flow, and — with ``--verify`` — resolves them against the signed-in
app and user.

    python -m tests.preflight                 # the matrix, offline
    python -m tests.preflight --verify        # ... and what this tenant grants
    python -m tests.preflight --report rpt/   # rpt/preflight.md + rpt/preflight.json

The matrix is derived from the decorators stamped by :mod:`tests.decorators`; there is
no list of scopes anywhere in this file to fall out of date.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from datetime import datetime, timezone
from inspect import getmembers, isfunction
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest import TestCase

from office365.graph_client import GraphClient

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
    return None  # app-only-cert signs in through SharePoint, not Graph


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


def grant_plan(found: list[Needs], states: dict[Requirement, TenantState]) -> dict[str, list[str]]:
    """The smallest set of permissions that would unblock the suites, group by group.

    Every group is an any-of, so granting *one* of its names is enough — granting all of
    them would ask for more than any test needs. A name that appears in several unmet
    groups is asked for once. Groups this wizard cannot grant are still returned: the
    caller decides what to do with them, and silence would be a lie.
    """
    by_label: dict[str, list[tuple[str, ...]]] = {}
    for needs in found:
        for requirement, _ in needs.unmet_for(states):
            for label, names in requirement.shortfall(states[requirement]):
                by_label.setdefault(label, []).append(names)
    plan: dict[str, list[str]] = {}
    for label, groups in by_label.items():
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
        plan[label] = chosen
    return plan


def render_plan(plan: dict[str, list[str]]) -> str:
    """The plan as a short list a person can approve, one line per group."""
    lines = []
    for label in sorted(plan):
        names = plan[label]
        lines.append(f"  {label:<15} {', '.join(names)}")
    return "\n".join(lines)


def _flow_status(flow: str) -> str:
    missing = settings.missing_for(flow)
    return f"not configured (missing: {', '.join(missing)})" if missing else "configured"


def render_markdown(found: list[Needs], states: dict[Requirement, TenantState]) -> str:
    """The report: what every live suite needs, and what this environment answers."""
    lines = [
        "# Live-test preflight",
        "",
        f"Generated by `python -m tests.preflight` for tenant `{settings.tenant or '<none>'}`.",
        "",
        "## Auth flows",
        "",
        "| flow | state |",
        "| --- | --- |",
    ]
    lines += [f"| {FLOWS[flow].label} (`{flow}`) | {_flow_status(flow)} |" for flow in FLOWS]

    total_tests = sum(needs.tests for needs in found)
    total_requirements = sum(len(needs.requirements) for needs in found)
    lines += [
        "",
        f"{len(found)} live suites, {total_tests} live tests, {total_requirements} declared permission requirements.",
        "",
        "## Suites",
        "",
        "| suite | flow | tests | declared | status |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for needs in found:
        if not needs.requirements:
            lines.append(f"| `{needs.suite}` | `{needs.flow}` | {needs.tests} | none declared | credentials only |")
            continue
        for requirement in sorted(needs.requirements, key=_ordered):
            tests = len(needs.requirements[requirement])
            status = _status(requirement, states)
            lines.append(f"| `{needs.suite}` | `{needs.flow}` | {tests} | {requirement.describe()} | {status} |")

    missing = [(needs, requirement, tests) for needs in found for requirement, tests in needs.unmet_for(states)]
    if states:
        lines += ["", "## Missing", ""]
        if not missing:
            lines.append("Every declared requirement is met.")
        for needs, requirement, tests in missing:
            lines.append(f"- `{needs.suite}`: {requirement.describe()} — {len(tests)} test(s), e.g. `{tests[0]}`")
    else:
        lines += [
            "",
            "## Missing",
            "",
            "Not verified: run with `--verify` (needs credentials) to resolve these against the tenant.",
        ]
    return "\n".join(lines) + "\n"


def _status(requirement: Requirement, states: dict[Requirement, TenantState]) -> str:
    state = states.get(requirement)
    if state is None:
        return "not verified"
    if state.unverifiable:
        return f"not verified ({state.unverifiable})"
    unmet = requirement.unmet(state)
    return "met" if not unmet else "missing " + " and ".join(unmet)


def render_json(found: list[Needs], states: dict[Requirement, TenantState]) -> str:
    """The same report for CI: flows, suites, requirements and their status."""
    payload: dict[str, Any] = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tenant": settings.tenant,
        "flows": {flow: {"label": FLOWS[flow].label, "missing": settings.missing_for(flow)} for flow in FLOWS},
        "suites": [
            {
                "suite": needs.suite,
                "flow": needs.flow,
                "tests": needs.tests,
                "requirements": [
                    {
                        "declared": requirement.describe(),
                        "status": _status(requirement, states),
                        "tests": needs.requirements[requirement],
                    }
                    for requirement in sorted(needs.requirements, key=_ordered)
                ],
            }
            for needs in found
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
    parser.add_argument("--report", metavar="DIR", help="write preflight.md into DIR (a report for people)")
    parser.add_argument("--json", metavar="DIR", help="write preflight.json into DIR (a report for tools)")
    parser.add_argument("--strict", action="store_true", help="exit 1 when a flow or requirement is not satisfied")
    args = parser.parse_args(argv)

    found = suites()
    # --strict cannot mean anything without an answer to compare against, so it verifies too.
    states = verify(found, settings.client_id) if (args.verify or args.strict) else {}
    markdown = render_markdown(found, states)
    if not (args.report or args.json):
        sys.stdout.write(markdown)
    if args.report:
        print(f"Wrote {_write(Path(args.report), markdown, 'preflight.md')}")
    if args.json:
        print(f"Wrote {_write(Path(args.json), render_json(found, states), 'preflight.json')}")

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
