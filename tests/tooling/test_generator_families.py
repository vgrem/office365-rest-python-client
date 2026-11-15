"""The security tree's families are a rule, not a habit.

``*AuditRecord`` belongs in ``audit/records`` and ``*Evidence`` in ``alerts/evidence``.
Until the families were a table the descent placed them by their opening word, so a new
record landed flat in ``audit/`` and the folder had to be repaired by hand every time.
These tests pin the rule on the tree it governs and on two types that do not exist yet.
"""

from __future__ import annotations

import ast
from pathlib import Path

from generator.planning.families import FAMILIES, family_target
from generator.planning.routing import descend_module

_ROOT = Path(__file__).resolve().parents[2]
_OUTPUT_BASE = str(_ROOT / "office365")
_SECURITY = _ROOT / "office365" / "security"


def _classes(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [node.name for node in tree.body if isinstance(node, ast.ClassDef)]


def _modules_ending_with(suffix: str, root: Path = _SECURITY) -> list[tuple[str, str]]:
    """``(relative path, class name)`` for every model below ``root`` ending with ``suffix``."""
    found = []
    for path in sorted(root.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        for name in _classes(path):
            if name.endswith(suffix):
                found.append((path.relative_to(_ROOT).as_posix(), name))
    return found


def test_every_audit_record_sits_under_audit_records() -> None:
    """The family is the audit feed's: a record lives nowhere else in ``audit/``."""
    misplaced = [path for path, _ in _modules_ending_with("AuditRecord", _SECURITY / "audit") if "/records/" not in path]
    assert misplaced == []


def test_every_alert_evidence_sits_under_alerts_evidence() -> None:
    """``alerts/`` reads evidence from one folder -- the base class included."""
    misplaced = [path for path, _ in _modules_ending_with("Evidence", _SECURITY / "alerts") if "/evidence/" not in path]
    assert misplaced == []


def test_every_family_names_a_folder_the_tree_has() -> None:
    """A family whose folder is missing silently falls back to the word-prefix descent."""
    assert [family.folder for family in FAMILIES if not (_ROOT / "office365" / family.folder).is_dir()] == []


def test_a_new_record_lands_in_the_folder_that_reads_it() -> None:
    # ``VivaAuditRecord``'s opening word is a source, so the source folder claims it.
    assert descend_module("office365.security.audit", "VivaAuditRecord", _OUTPUT_BASE) == (
        "office365.security.audit.records.viva",
        "audit_record",
    )
    # An unknown source keeps its word: no folder is created to shorten the stem.
    assert descend_module("office365.security.audit", "FabricAuditRecord", _OUTPUT_BASE) == (
        "office365.security.audit.records",
        "fabric_audit_record",
    )


def test_a_family_does_not_reach_outside_its_subtree() -> None:
    """``SimulationStatus`` is an attack simulation's, not an alert's."""
    assert family_target("office365.security.attacksimulations", "SimulationStatus", _OUTPUT_BASE) is None
    assert family_target("office365.security.alerts", "AlertStatus", _OUTPUT_BASE) == (
        "office365.security.alerts.states",
        "alert",
    )
