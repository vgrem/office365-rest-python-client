"""Pytest configuration.

Test conventions:
- Plain ``unittest.TestCase`` under ``tests/unit/`` = offline unit tests that run
  with no credentials and are always executed. They assert a *value* or a
  *decision* the client derives before it sends anything (a parsed object, the
  bytes it would emit, a checksum, an idempotency rule, an error's type). A test
  whose subject is the exchange itself -- the URL, the header, the batch
  envelope, the paging loop, the transfer loop -- is not a unit test here: the
  product suites below pin those against a real tenant, which is the only
  authority on them.
- ``SPTestCase`` / ``GraphDelegatedTestCase`` subclasses = live integration tests
  that require tenant credentials. They are skipped automatically when the
  matching credentials are not configured, so a fresh checkout stays green.

Use ``--offline`` to skip every live test explicitly (what CI runs), or
``python -m tests.doctor`` to see what is configured.
"""

from __future__ import annotations

from collections.abc import Iterable

import pytest

from tests.preflight import flow_of
from tests.settings import FLOWS, settings

#: Missing requirements per flow, computed once for the whole session.
_READINESS = settings.readiness()

#: Flows that ended up skipped because their credentials were missing.
_SKIPPED_FLOWS: pytest.StashKey[set[str]] = pytest.StashKey()


#: How the report is produced; quoted in the summary so the command is copy-pasteable.
_PREFLIGHT = "python -m tests.preflight --verify --report tests-report"


def _flow_for(item: pytest.Item) -> str | None:
    """Return the auth flow a live test class needs, or ``None`` for offline tests."""
    cls = getattr(item, "cls", None)
    return None if cls is None else flow_of(cls)


def _permission_skips(terminalreporter: pytest.TerminalReporter) -> dict[str, int]:
    """Count the tests a signed-in run skipped because the tenant lacked a permission."""
    reasons: dict[str, int] = {}
    for report in terminalreporter.stats.get("skipped", []):
        # A skip's longrepr is ("path", lineno, "Skipped: <reason>") rather than a crash report.
        longrepr = report.longrepr
        message = str(longrepr[-1]) if isinstance(longrepr, tuple) else str(longrepr)
        _, marker, declared = message.partition("Skipped: missing ")
        if marker:
            reasons[declared.strip()] = reasons.get(declared.strip(), 0) + 1
    return reasons


def pytest_addoption(parser: pytest.Parser) -> None:
    """Support command line marks."""
    parser.addoption("--offline", action="store_true", help="skip all live integration tests")


def pytest_configure(config: pytest.Config) -> None:
    config.stash[_SKIPPED_FLOWS] = set()


def pytest_report_header(config: pytest.Config) -> str:
    """Show, up front, which auth flows are configured."""
    if config.getoption("--offline"):
        return "auth: live tests disabled (--offline)"
    parts = [f"{flow}: {'off' if missing else 'on'}" for flow, missing in _READINESS.items()]
    return "auth: " + " | ".join(parts)


def pytest_collection_modifyitems(config: pytest.Config, items: Iterable[pytest.Item]) -> None:
    """Skip live tests whose credentials are not configured (or when ``--offline``)."""
    offline = config.getoption("--offline")
    skipped: set[str] = config.stash[_SKIPPED_FLOWS]

    for item in items:
        flow = _flow_for(item)
        if flow is None:
            continue

        if offline:
            item.add_marker(pytest.mark.skip(reason="--offline: live integration tests are skipped"))
            continue

        missing = _READINESS[flow]
        if missing:
            skipped.add(flow)
            item.add_marker(
                pytest.mark.skip(
                    reason=(
                        f"{flow} credentials are not configured (missing: {', '.join(missing)}). "
                        "Copy .env.example to .env, run `python -m tests.doctor`, or pass --offline."
                    )
                )
            )


def pytest_terminal_summary(terminalreporter: pytest.TerminalReporter, exitstatus: int, config: pytest.Config) -> None:
    """Explain the skips: missing credentials first, then permissions the tenant denied."""
    if config.getoption("--offline"):
        return
    skipped: set[str] = config.stash[_SKIPPED_FLOWS]
    if skipped:
        terminalreporter.write_sep("=", "auth credentials not configured")
        for flow in sorted(skipped):
            missing = _READINESS[flow]
            terminalreporter.write_line(f"{FLOWS[flow].label}: missing {', '.join(missing)}")
        terminalreporter.write_line("Copy .env.example to .env and fill it in, then run `python -m tests.doctor`.")
        terminalreporter.write_line("Pass --offline to make this quiet.")
    _report_permission_skips(terminalreporter, config)


def _report_permission_skips(terminalreporter: pytest.TerminalReporter, config: pytest.Config) -> None:
    """Say which permissions this tenant denied, instead of leaving a bare skip count."""
    if config.getoption("--offline"):
        return
    reasons = _permission_skips(terminalreporter)
    if reasons:
        terminalreporter.write_sep("=", "permissions this tenant did not grant")
        for declared, count in sorted(reasons.items(), key=lambda item: (-item[1], item[0])):
            terminalreporter.write_line(f"{count:4d}  {declared}")
    terminalreporter.write_line(f"Full matrix and remediation: `{_PREFLIGHT}`")
