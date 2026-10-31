"""Tests for the web-scope site-settings copy (offline).

The site-level verify pass that reports what the copy left behind lives here too.
"""

from __future__ import annotations

import json

import pytest
from office365.migration.sharepoint import site_verify
from office365.migration.sharepoint.resolvers import (
    _apply_web_settings,  # pyright: ignore[reportPrivateUsage]
)
from office365.migration.sharepoint.site_settings import (
    apply_web_settings,
)
from office365.migration.sharepoint.site_verify import (
    SITE_SCOPE,
    WEB_SCOPE_STRUCTURE,
    verify_site,
)
from office365.migration.sharepoint.verify import StructureReport


class _Web:
    """A web that records the projected GET, the MERGE, and the values written."""

    def __init__(self, title=None, description=None, url="https://contoso.sharepoint.com/sites/t"):
        self._props = {"Url": url, "Title": title, "Description": description}
        self.selected = None
        self.written = {}
        self.updates = 0
        self.fail_update = False

    @property
    def properties(self):
        return self._props

    @property
    def url(self):
        return self._props.get("Url")

    @property
    def server_relative_url(self):
        return self._props.get("ServerRelativeUrl")

    def get_property(self, name):
        return self._props.get(name)

    def select(self, names):
        self.selected = names
        return self

    def set_property(self, name, value):
        self.written[name] = value
        self._props[name] = value
        return self

    def get(self):
        return self

    def update(self):
        if self.fail_update:
            raise RuntimeError("boom")
        self.updates += 1
        return self

    def execute_query(self):
        return self


def test_apply_web_settings_copies_only_differing_values():
    source = _Web(title="Source", description="Same")
    target = _Web(title="Target", description="Same")

    report = apply_web_settings(source, target)

    assert target.written == {"Title": "Source"}
    assert target.updates == 1
    assert report.changed is True
    assert report.applied == {"Title": "Source"}
    assert report.summary() == "site settings: copied Title onto https://contoso.sharepoint.com/sites/t"


def test_a_failing_copy_degrades_to_a_warning():
    source = _Web(title="Source")
    target = _Web(title="Target")
    target.fail_update = True
    warnings: list[str] = []

    report = _apply_web_settings(source, target, True, warnings)

    assert report is None
    assert len(warnings) == 1
    assert warnings[0].startswith("site settings copy failed for https://contoso.sharepoint.com/sites/t")


# --- verify_site: what the copy left behind -----------------------------------


class _VerifyWeb:
    def __init__(self, url="https://contoso.sharepoint.com/sites/team_out"):
        self.url = url
        self.context = type("_Context", (), {"base_url": "https://contoso.sharepoint.com/sites/team_out"})()


class _Context:
    def __init__(self, web):
        self.web = web


@pytest.fixture
def contexts():
    return _Context(_Web("https://contoso.sharepoint.com/sites/team_in")), _Context(_VerifyWeb())


@pytest.fixture
def clean(monkeypatch):
    """Every web-level verifier returns no findings, and records its calls."""
    calls = []

    def _note(name):
        def _run(source_web, target_web):
            calls.append(name)
            return []

        return _run

    for name, func in (
        ("settings", "verify_web_settings"),
        ("branding", "verify_web_branding"),
        ("navigation", "verify_navigation"),
        ("pages", "verify_page_copy"),
        ("security", "verify_site_security"),
        ("list security", "verify_list_security"),
    ):
        monkeypatch.setattr(site_verify, func, _note(name))
    monkeypatch.setattr(site_verify, "_web_scope_findings", _note("web-scope"))
    monkeypatch.setattr(site_verify, "_site_scope_findings", _note(SITE_SCOPE))
    return calls


def test_a_clean_web_is_ok_and_complete(contexts, clean):
    report = verify_site(*contexts)

    assert report.ok
    assert report.complete
    assert report.issues == []
    assert report.url == "https://contoso.sharepoint.com/sites/team_out"
    assert report.findings == {}
    assert report.checked == ["settings", "branding", WEB_SCOPE_STRUCTURE, SITE_SCOPE]
    assert report.summary() == (
        "OK | https://contoso.sharepoint.com/sites/team_out | settings: 0, branding: 0, "
        "web-scope structure: 0, site scope: 0"
    )
    assert json.loads(json.dumps(report.to_dict()))["ok"] is True


def test_a_failing_list_report_makes_the_web_a_mismatch(contexts, clean, monkeypatch):
    monkeypatch.setattr(
        site_verify,
        "verify_list_structure",
        lambda s, t: StructureReport(list_title=t, missing_columns=["Region"]),
    )

    report = verify_site(*contexts, lists=[("source", "target")])

    assert not report.ok
    assert report.summary().startswith("OK") is False
    assert report.summary().startswith("MISMATCH")
    assert "lists: 1 (1 with issues)" in report.summary()
    assert report.issues == [
        "MISMATCH | target | columns: 1, content types: 0, views: 0, field links: 0, settings: 0, "
        "column attributes: 0, formatting: 0"
    ]
