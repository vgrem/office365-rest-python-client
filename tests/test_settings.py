"""Offline tests for test/example configuration path handling.

Regression coverage: path values configured in ``.env`` are documented relative
to the repository root (e.g. ``OFFICE365_CERT_PATH=tests/selfsigncert.pem``).
They must keep working when an example or test is launched from a nested
working directory, so relative paths are anchored to ``PROJECT_ROOT`` rather
than the current directory.
"""

from __future__ import annotations

import os
import unittest
from pathlib import Path
from unittest import mock

from tests.settings import FLOWS, PROJECT_ROOT, Settings, _resolve_path


class TestResolvePath(unittest.TestCase):
    def test_relative_path_is_anchored_to_project_root(self) -> None:
        resolved = Path(_resolve_path("tests/selfsigncert.pem"))
        self.assertTrue(resolved.is_absolute())
        self.assertEqual(resolved, PROJECT_ROOT / "tests" / "selfsigncert.pem")

    def test_absolute_path_is_preserved(self) -> None:
        absolute = str(Path(PROJECT_ROOT) / "tests" / "selfsigncert.pem")
        self.assertEqual(_resolve_path(absolute), absolute)

    def test_home_is_expanded(self) -> None:
        resolved = Path(_resolve_path("~/cert.pem"))
        self.assertTrue(resolved.is_absolute())
        self.assertEqual(resolved, Path.home() / "cert.pem")

    def test_from_env_resolves_relative_cert_path(self) -> None:
        with mock.patch.dict(os.environ, {"OFFICE365_CERT_PATH": "tests/selfsigncert.pem"}):
            settings = Settings.from_env()
        self.assertEqual(Path(settings.cert_path), PROJECT_ROOT / "tests" / "selfsigncert.pem")

    def test_from_env_default_cert_path_is_absolute(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("OFFICE365_CERT_PATH", None)
            settings = Settings.from_env()
        self.assertTrue(Path(settings.cert_path).is_absolute())


class TestReadinessReport(unittest.TestCase):
    """The banner `doctor` and `setup` print: one line per flow, the tip only when nothing is ready."""

    def test_every_flow_is_named_with_what_it_is_missing(self) -> None:
        report = Settings().format_readiness()
        self.assertIn("Auth readiness (environment + .env):", report)
        for label in (spec.label for spec in FLOWS.values()):
            self.assertIn(label, report)
        self.assertNotIn("  ready", report)
        self.assertIn("  Tip: run `python -m tests.setup`", report)

    def test_a_configured_flow_reads_ready_and_silences_the_tip(self) -> None:
        report = Settings(tenant="contoso.onmicrosoft.com", client_id="app-id").format_readiness()
        self.assertIn("ready", report)
        self.assertNotIn("Tip: run", report)


if __name__ == "__main__":
    unittest.main()
