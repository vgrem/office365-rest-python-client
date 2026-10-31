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

from tests.settings import FLOWS, PROJECT_ROOT, EnvFile, Settings, _resolve_path, derived_urls


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


class TestEnvFile(unittest.TestCase):
    """The `.env` grammar `tests.settings` loads and `tests.setup` writes."""

    def _file(self, text: str = "") -> EnvFile:
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, True)
        env = EnvFile(folder / ".env", folder / ".env.example")
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

    def test_merge_replaces_in_place_and_only_fills_an_empty_value(self) -> None:
        env = self._file("# header\nOFFICE365_TENANT=old\nOFFICE365_SITE_URL=\nUNRELATED=kept\n")
        text = env.merge(
            overrides={"OFFICE365_TENANT": "contoso.onmicrosoft.com"},
            defaults={"OFFICE365_SITE_URL": "https://contoso.sharepoint.com"},
        )
        self.assertEqual(
            text,
            "# header\nOFFICE365_TENANT=contoso.onmicrosoft.com\nOFFICE365_SITE_URL=https://contoso.sharepoint.com\n"
            "UNRELATED=kept\n",
        )

    def test_a_default_never_overwrites_a_configured_value(self) -> None:
        env = self._file("OFFICE365_SITE_URL=https://mine.sharepoint.com\n")
        text = env.merge({}, {"OFFICE365_SITE_URL": "https://derived.sharepoint.com"})
        self.assertEqual(text, "OFFICE365_SITE_URL=https://mine.sharepoint.com\n")

    def test_a_key_the_file_does_not_have_is_appended_under_one_comment(self) -> None:
        env = self._file("OFFICE365_TENANT=contoso.onmicrosoft.com\n")
        text = env.merge({"OFFICE365_CLIENT_ID": "app-id"}, {})
        self.assertTrue(text.endswith("# Added by python -m tests.setup\nOFFICE365_CLIENT_ID=app-id\n"))

    def test_the_environment_wins_over_the_file(self) -> None:
        env = self._file("OFFICE365_TENANT=from-file\n")
        with mock.patch.dict(os.environ, {"OFFICE365_TENANT": "from-shell"}):
            env.load()
            self.assertEqual(os.environ["OFFICE365_TENANT"], "from-shell")

    def test_a_missing_file_reads_as_nothing_and_loads_without_failing(self) -> None:
        env = self._file()
        self.assertEqual(env.read(), {})
        self.assertEqual(env.source_lines(), [])
        env.load()

    def test_the_source_is_the_env_file_when_present_else_the_template(self) -> None:
        env = self._file()
        env.example.write_text("OFFICE365_TENANT=\n", encoding="utf-8")
        self.assertEqual(env.source_lines(), ["OFFICE365_TENANT="])
        env.path.write_text("OFFICE365_TENANT=contoso.onmicrosoft.com\n", encoding="utf-8")
        self.assertEqual(env.source_lines(), ["OFFICE365_TENANT=contoso.onmicrosoft.com"])

    def test_redact_hides_the_secrets_and_leaves_the_rest(self) -> None:
        text = "OFFICE365_TENANT=contoso\nOFFICE365_CLIENT_SECRET=s3cret\nOFFICE365_PASSWORD=pw # note\n"
        self.assertEqual(
            self._file().redact(text),
            "OFFICE365_TENANT=contoso\nOFFICE365_CLIENT_SECRET=<hidden>\nOFFICE365_PASSWORD=<hidden>",
        )


class TestDerivedUrls(unittest.TestCase):
    """One derivation per URL shape, shared by the loader and the setup wizard."""

    def test_a_tenant_name_alone_determines_the_site_urls(self) -> None:
        urls = derived_urls("contoso")
        self.assertEqual(urls["OFFICE365_ROOT_SITE_URL"], "https://contoso.sharepoint.com")
        self.assertEqual(urls["OFFICE365_SITE_URL"], "https://contoso.sharepoint.com")
        self.assertEqual(urls["OFFICE365_TEAM_SITE_URL"], "https://contoso.sharepoint.com/sites/team")
        self.assertEqual(urls["OFFICE365_ADMIN_SITE_URL"], "https://contoso-admin.sharepoint.com")
        self.assertEqual(urls["OFFICE365_CONTENT_TYPE_HUB_URL"], "https://contoso.sharepoint.com/sites/contentTypeHub")

    def test_an_explicit_root_wins_and_the_children_follow_it(self) -> None:
        urls = derived_urls("contoso", "https://contoso.sharepoint.com/sites/project")
        self.assertEqual(urls["OFFICE365_SITE_URL"], "https://contoso.sharepoint.com/sites/project")
        self.assertEqual(urls["OFFICE365_TEAM_SITE_URL"], "https://contoso.sharepoint.com/sites/project/sites/team")

    def test_nothing_is_derived_without_a_tenant_name(self) -> None:
        self.assertEqual(derived_urls(""), {"OFFICE365_TENANT_PREFIX": "", "OFFICE365_ROOT_SITE_URL": ""})

    def test_the_loader_reads_the_derived_urls_when_the_environment_is_silent(self) -> None:
        with mock.patch.dict(os.environ, {"OFFICE365_TENANT": "contoso.onmicrosoft.com"}, clear=True):
            settings = Settings.from_env()
        self.assertEqual(settings.tenant_prefix, "contoso")
        self.assertEqual(settings.site_url, "https://contoso.sharepoint.com")
        self.assertEqual(settings.admin_site_url, "https://contoso-admin.sharepoint.com")

    def test_the_loader_prefers_an_explicit_url_over_the_derived_one(self) -> None:
        explicit = {"OFFICE365_TENANT": "contoso.onmicrosoft.com", "OFFICE365_SITE_URL": "https://mine.sharepoint.com"}
        with mock.patch.dict(os.environ, explicit, clear=True):
            settings = Settings.from_env()
        self.assertEqual(settings.site_url, "https://mine.sharepoint.com")
        self.assertEqual(settings.team_site_url, "https://contoso.sharepoint.com/sites/team")


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
