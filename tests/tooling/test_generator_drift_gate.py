"""The drift gate: a snapshot that wants a write fails the run, a preview does not.

The generator could always *say* "nothing to do" -- it prints the counts and exits 0
either way. So the tree could drift from the snapshot (a refreshed CSDL nobody
regenerated, a member dropped by hand) with every check green. ``--fail-on-write`` is
that sentence as an exit code.

The same doctored snapshot runs both ways here, so what decides is the flag, not the
drift. A clean tree exiting 0 is what CI asserts on every build; asserting it in this
file would make it fail on any developer's local drift.
"""

from __future__ import annotations

from pathlib import Path

from generator.cli import main

_ROOT = Path(__file__).resolve().parents[2]
_SNAPSHOT = _ROOT / "generator" / "metadata" / "SharePoint.xml"
#: ``SP.File`` is declared without a base type, which is what makes this anchor unique:
#: the other ``Name="File"`` in the snapshot is ``MS.FileServices.FileSystemItem``.
_FILE = '<EntityType Name="File">'


def _snapshot_declaring_a_member_the_tree_lacks(tmp_path: Path) -> str:
    source = _SNAPSHOT.read_text(encoding="utf-8")
    assert source.count(_FILE) == 1
    doctored = source.replace(_FILE, _FILE + '\n        <Property Name="ZzDriftProbe" Type="Edm.String"/>', 1)
    path = tmp_path / "SharePoint.xml"
    path.write_text(doctored, encoding="utf-8")
    return str(path)


def test_the_flag_decides_the_exit_code_not_the_preview(tmp_path: Path) -> None:
    argv = [
        "sharepoint",
        "--type",
        "SP.File",
        "--metadata",
        _snapshot_declaring_a_member_the_tree_lacks(tmp_path),
        "--dry-run",
    ]

    assert main(argv) == 0
    assert main([*argv, "--fail-on-write"]) == 1
