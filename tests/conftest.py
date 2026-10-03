"""Pytest configuration.

Test conventions:
- Plain ``unittest.TestCase`` under ``tests/unit/`` = offline unit tests that run
  with no credentials and are always executed.
- ``SPTestCase`` / ``GraphDelegatedTestCase`` subclasses = live integration tests
  that require tenant credentials. They are skipped automatically when the
  matching credentials are not configured, so a fresh checkout stays green.

Use ``--offline`` to skip every live test explicitly (what CI runs), or
``python -m tests.doctor`` to see what is configured.
"""

from __future__ import annotations

from collections.abc import Iterable

import pytest

from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase
from tests.settings import FLOWS, settings
from tests.sharepoint.sharepoint_case import SPTestCase

#: Missing requirements per flow, computed once for the whole session.
_READINESS = settings.readiness()

#: Flows that ended up skipped because their credentials were missing.
_SKIPPED_FLOWS: pytest.StashKey[set[str]] = pytest.StashKey()


def _flow_for(item: pytest.Item) -> str | None:
    """Return the auth flow a live test class needs, or ``None`` for offline tests."""
    cls = getattr(item, "cls", None)
    if cls is None:
        return None
    # GraphApplicationTestCase subclasses GraphDelegatedTestCase, so check it first.
    if issubclass(cls, GraphApplicationTestCase):
        return "app-only"
    if issubclass(cls, GraphDelegatedTestCase):
        return "delegated-ropc"
    if issubclass(cls, SPTestCase):
        return "app-only-cert"
    return None


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
    """Explain any credential-based skips instead of silently doing nothing."""
    if config.getoption("--offline"):
        return
    skipped: set[str] = config.stash[_SKIPPED_FLOWS]
    if not skipped:
        return

    terminalreporter.write_sep("=", "auth credentials not configured")
    for flow in sorted(skipped):
        missing = _READINESS[flow]
        terminalreporter.write_line(f"{FLOWS[flow].label}: missing {', '.join(missing)}")
    terminalreporter.write_line("Copy .env.example to .env and fill it in, then run `python -m tests.doctor`.")
    terminalreporter.write_line("Pass --offline to make this quiet.")
