"""CLI dispatch: subcommand words map onto the flat flags, which keep working."""

from __future__ import annotations

from generator import cli


def test_subcommand_expands_to_flag() -> None:
    assert cli.expand_subcommand(["fetch", "graph"]) == ["graph", "--fetch"]
    assert cli.expand_subcommand(["routing", "sharepoint"]) == ["sharepoint", "--suggest-routing"]


def test_generate_subcommand_adds_no_flag() -> None:
    assert cli.expand_subcommand(["generate", "graph", "--dry-run"]) == ["graph", "--dry-run"]


def test_legacy_flags_pass_through() -> None:
    argv = ["graph", "--suggest-routing"]
    assert cli.expand_subcommand(argv) == argv


def test_fetch_subcommand_dispatches(monkeypatch) -> None:
    seen = {}

    def stub(service, version, path):
        seen.update(service=service, version=version, path=path)
        return "x.xml"

    monkeypatch.setattr("generator.metadata.fetch.fetch", stub)

    assert cli.main(["fetch", "graph", "--graph-version", "beta"]) == 0
    assert seen == {"service": "graph", "version": "beta", "path": None}
