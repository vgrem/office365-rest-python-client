"""Offline tests for test/example configuration path handling.

Regression coverage: path values configured in ``.env`` are documented relative
to the repository root (e.g. ``OFFICE365_CERT_PATH=tests/selfsigncert.pem``).
They must keep working when an example or test is launched from a nested
working directory, so relative paths are anchored to ``PROJECT_ROOT`` rather
than the current directory.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.settings import PROJECT_ROOT, EnvFile, Settings


class TestResolvePath(unittest.TestCase):
    """A relative path in `.env` is read against the repository, not the working directory."""

    def test_from_env_resolves_relative_cert_path(self) -> None:
        with mock.patch.dict(os.environ, {"OFFICE365_CERT_PATH": "tests/selfsigncert.pem"}):
            settings = Settings.from_env()
        self.assertEqual(Path(settings.cert_path), PROJECT_ROOT / "tests" / "selfsigncert.pem")


class TestEnvFile(unittest.TestCase):
    """The `.env` grammar `tests.settings` reads: one parser, and nothing that writes."""

    def _file(self, text: str = "") -> EnvFile:
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, True)
        env = EnvFile(folder / ".env")
        if text:
            env.path.write_text(text, encoding="utf-8")
        return env

    def test_a_value_keeps_a_comment_only_when_it_is_quoted(self) -> None:
        env = self._file(
            "\n".join(
                [
                    "# a comment",
                    "",
                    "export OFFICE365_TENANT=contoso.onmicrosoft.com",
                    "OFFICE365_SITE_URL=https://contoso.sharepoint.com  # the root",
                    "OFFICE365_TEAM_SITE_URL='https://contoso.sharepoint.com/sites/team'",
                    "not an assignment",
                ]
            )
        )
        self.assertEqual(
            env.read(),
            {
                "OFFICE365_TENANT": "contoso.onmicrosoft.com",
                "OFFICE365_SITE_URL": "https://contoso.sharepoint.com",
                "OFFICE365_TEAM_SITE_URL": "https://contoso.sharepoint.com/sites/team",
            },
        )

    def test_the_environment_wins_over_the_file(self) -> None:
        env = self._file("OFFICE365_TENANT=from-file\n")
        with mock.patch.dict(os.environ, {"OFFICE365_TENANT": "from-shell"}):
            env.load()
            self.assertEqual(os.environ["OFFICE365_TENANT"], "from-shell")

    def test_a_missing_file_reads_as_nothing_and_loads_without_failing(self) -> None:
        env = self._file()
        self.assertEqual(env.read(), {})
        env.load()


class TestReadinessReport(unittest.TestCase):
    """The banner `doctor` and `setup` print: the tip appears only when no flow is ready."""

    def test_the_tip_is_shown_only_when_no_flow_is_ready(self) -> None:
        self.assertNotIn("  ready", Settings().format_readiness())
        self.assertIn("Tip: run `python -m tests.setup`", Settings().format_readiness())

        configured = Settings(tenant="contoso.onmicrosoft.com", client_id="app-id").format_readiness()
        self.assertIn("ready", configured)
        self.assertNotIn("Tip: run", configured)


if __name__ == "__main__":
    unittest.main()
