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
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest import TestCase

from office365.graph_client import GraphClient

from tests.capabilities import Needs, Requirement, TenantState, declared_requirement
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase
from tests.settings import FLOWS, settings
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
        test_names = [attr for attr in dir(obj) if attr.startswith("test")]
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


def _client(flow: str) -> GraphClient | None:
    """A signed-in Graph client for ``flow``, or ``None`` when it cannot be built here."""
    if not settings.is_ready(flow):
        return None
    client = GraphClient(tenant=settings.tenant)
    if flow == "delegated-ropc":
        return client.with_username_and_password(settings.client_id, settings.username, settings.password)
    if flow == "app-only":
        return client.with_client_secret(settings.client_id, settings.client_secret)
    return None  # app-only-cert signs in through SharePoint, not Graph


def verify(found: list[Needs], client_id: str) -> dict[Requirement, TenantState]:
    """Resolve every declared requirement against the tenant, once per requirement."""
    states: dict[Requirement, TenantState] = {}
    for flow in sorted({needs.flow for needs in found}):
        required = {requirement for needs in found if needs.flow == flow for requirement in needs.requirements}
        try:
            client = _client(flow)
            if client is None:
                continue
            for requirement in required:
                states[requirement] = TenantState.of(client, client_id, requirement)
        except Exception as error:  # noqa: BLE001 - a report must survive one bad flow, not die on it
            failure = TenantState(unverifiable=f"signing in failed: {error}")
            states.update(dict.fromkeys(required, failure))
    return states


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
    parser.add_argument("--report", metavar="DIR", help="write preflight.md and preflight.json into DIR")
    parser.add_argument("--strict", action="store_true", help="exit 1 when a flow or requirement is not satisfied")
    args = parser.parse_args(argv)

    found = suites()
    # --strict cannot mean anything without an answer to compare against, so it verifies too.
    states = verify(found, settings.client_id) if (args.verify or args.strict) else {}
    markdown = render_markdown(found, states)
    if args.report:
        directory = Path(args.report)
        print(f"Wrote {_write(directory, markdown, 'preflight.md')}")
        print(f"Wrote {_write(directory, render_json(found, states), 'preflight.json')}")
    else:
        sys.stdout.write(markdown)

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
