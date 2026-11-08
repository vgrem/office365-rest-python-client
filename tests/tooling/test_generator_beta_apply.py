"""What the marker pass writes where a member has no declaration to extend.

A property carries its ``@odata(name=...)`` already, so a marker is one argument added to a
line that exists. An operation carries nothing -- its wire name was, until now, only the
string its query was built with -- so the pass has to write the declaration whole, above the
``def``, and keep the operation out of ``$select`` while it is there.

This file deliberately does not cover the other half: which markers the snapshot pair
justifies. That is ``generator.tools.beta_markers``, decided before a line is touched.
"""

import ast
from pathlib import Path

from generator.tools.beta_markers import MarkerEdits, MemberMarker
from generator.tools.marker_apply import TypeFiles, apply_markers

TYPE_NAME = "microsoft.graph.Widget"

_MODEL = '''
from __future__ import annotations

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery


class Widget(Entity):
    """A widget."""

    def entity_type_name(self):
        return "microsoft.graph.Widget"

    def stable_action(self) -> Self:
        """stableAction operation."""
        query = ServiceOperationQuery(self, "stableAction", None, {}, None, None)
        self.context.add_query(query)
        return self

    def preview_action(self) -> Self:
        """previewAction operation."""
        query = ServiceOperationQuery(self, "previewAction", None, {}, None, None)
        self.context.add_query(query)
        return self

    @odata(name="renamedAction", beta="betaRenamedAction")
    def renamed_action(self) -> Self:
        """renamedAction operation."""
        query = ServiceOperationQuery(self, "renamedAction", None, {}, None, None)
        self.context.add_query(query)
        return self
'''


def _tree(tmp_path: Path) -> Path:
    path = tmp_path / "office365" / "widget.py"
    path.parent.mkdir(parents=True)
    path.write_text(_MODEL, encoding="utf-8")
    return tmp_path


def _marker(member: str, beta=True) -> MemberMarker:
    return MemberMarker(type_name=TYPE_NAME, member=member, kind="method", beta=beta, reason="only the target")


def _apply(root: Path, *markers: MemberMarker, removed: bool = False) -> object:
    edits = MarkerEdits(
        added=[] if removed else list(markers),
        changed=[],
        removed=list(markers) if removed else [],
        types_added=[],
        types_removed=[],
    )
    return apply_markers(edits, TypeFiles(root))


def _decorators(path: Path, kind: str) -> dict:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == kind:
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and getattr(decorator.func, "id", None) == "odata":
                    found = {keyword.arg: getattr(keyword.value, "value", None) for keyword in decorator.keywords}
    return found


def test_a_stable_only_operation_is_declared_as_stable(tmp_path):
    """The other direction: the preview root dropped it, so a preview client must not call it."""
    root = _tree(tmp_path)
    path = root / "office365" / "widget.py"

    report = _apply(root, _marker("stableAction", beta=False))

    assert [edit.action for edit in report.edits] == ["added"]
    assert _decorators(path, "stable_action") == {
        "name": "stableAction",
        "beta": False,
        "selectable": False,
    }


def test_an_operation_is_declared_where_it_had_no_declaration(tmp_path):
    root = _tree(tmp_path)
    path = root / "office365" / "widget.py"

    report = _apply(root, _marker("previewAction"))

    assert [edit.action for edit in report.edits] == ["added"]
    assert _decorators(path, "preview_action") == {
        "name": "previewAction",
        "beta": True,
        "selectable": False,
    }


def test_an_operation_that_already_states_its_name_is_rewritten_in_place(tmp_path):
    """A renamed member's alternate spelling survives; only the version it belongs to moves."""
    root = _tree(tmp_path)
    path = root / "office365" / "widget.py"

    report = _apply(root, _marker("renamedAction", beta=False))

    assert [edit.action for edit in report.edits] == ["changed"]
    assert _decorators(path, "renamed_action") == {
        "name": "renamedAction",
        "beta": False,
        "selectable": False,
    }


def test_an_operation_the_tree_does_not_carry_is_reported_not_invented(tmp_path):
    root = _tree(tmp_path)

    report = _apply(root, _marker("missingAction"))

    assert report.edits == []
    assert [reason for _, reason in report.skipped] == ["no method of that name is generated"]


def test_a_removed_marker_takes_the_whole_declaration_with_it(tmp_path):
    """An operation the roots agree about has nothing to say about which root it is."""
    root = _tree(tmp_path)
    path = root / "office365" / "widget.py"
    _apply(root, _marker("previewAction"))

    report = _apply(root, _marker("previewAction"), removed=True)

    assert [edit.action for edit in report.edits] == ["removed"]
    assert _decorators(path, "preview_action") == {}
