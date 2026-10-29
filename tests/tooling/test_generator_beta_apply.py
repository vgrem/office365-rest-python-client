"""The apply pass writes what the snapshot pair justifies -- and takes back the rest.

``beta_markers`` decides; this is the half that types. So the tests are about the two
things that make it safe to run on every generation: a decorator that already says the
wanted thing is left alone (a run over an up-to-date model is a no-op), and a marker the
snapshots have stopped justifying is *removed* -- that is how a preview that went stable
stops being marked.
"""

from pathlib import Path

from generator.beta_markers import (
    BETA_ONLY,
    RENAMED,
    MarkerEdits,
    MarkerPlan,
    MemberMarker,
    VersionMarker,
    compare_markers,
    read_declared_markers,
    read_declared_versions,
)
from generator.marker_apply import TypeFiles, apply_markers

SOURCE = """from office365.runtime.types.odata_property import odata


class Widget(Entity):
    @odata(name="uid")
    @property
    def uid(self) -> Optional[str]:
        return self.properties.get("uid", None)

    @odata(name="mentions", navigation=True)
    @property
    def mentions(self):
        return self.properties.get("mentions", None)

    @odata(name="businessPhones", beta=False)
    @property
    def business_phones(self):
        return self.properties.get("businessPhones", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""

VALUE_SOURCE = """from dataclasses import dataclass


@dataclass
class Widget(ClientValue):
    is_mentioned: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""

BASE_SOURCE = """from office365.runtime.types.odata_property import odata


class Entity:
    @odata(name="createdDateTime", readonly=True)
    @property
    def created_date_time(self):
        return self.properties.get("createdDateTime", None)
"""


def _tree(tmp_path: Path, **files: str) -> TypeFiles:
    for name, source in files.items():
        (tmp_path / f"{name}.py").write_text(source, encoding="utf-8")
    return TypeFiles(tmp_path)


def _apply(edits: MarkerEdits, tmp_path: Path, **files: str):
    files = files or {"widget": SOURCE}
    return apply_markers(edits, _tree(tmp_path, **files))


def _apply_again(edits: MarkerEdits, tmp_path: Path):
    """Apply to the tree as it stands: the seeding helper would reset the file."""
    return apply_markers(edits, TypeFiles(tmp_path))


def _marker(member: str, beta, kind: str = "property") -> MemberMarker:
    return MemberMarker("microsoft.graph.Widget", member, kind, beta, BETA_ONLY)


def _text(tmp_path: Path, name: str = "widget") -> str:
    return (tmp_path / f"{name}.py").read_text(encoding="utf-8")


def test_a_beta_only_member_gains_its_marker(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("uid", True)], changed=[], removed=[]), tmp_path)

    assert '@odata(name="uid", beta=True)' in _text(tmp_path)
    assert [(edit.action, edit.member) for edit in report.edits] == [("added", "uid")]


def test_a_navigation_is_marked_after_its_name_not_at_the_end(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("mentions", True, "navigation")], changed=[], removed=[]), tmp_path)

    assert '@odata(name="mentions", beta=True, navigation=True)' in _text(tmp_path)
    assert report.edits[0].action == "added"


def test_a_rename_carries_the_preview_spelling(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("mentions", "widgetMentions")], changed=[], removed=[]), tmp_path)

    assert '@odata(name="mentions", beta="widgetMentions", navigation=True)' in _text(tmp_path)
    assert report.edits[0].after == '@odata(name="mentions", beta="widgetMentions", navigation=True)'


def test_a_marker_that_changed_is_replaced_not_stacked(tmp_path):
    report = _apply(MarkerEdits(added=[], changed=[_marker("businessPhones", True)], removed=[]), tmp_path)

    assert '@odata(name="businessPhones", beta=True)' in _text(tmp_path)
    assert _text(tmp_path).count("beta=") == 1
    assert [edit.action for edit in report.edits] == ["changed"]


def test_a_marker_the_snapshots_stop_justifying_is_removed(tmp_path):
    report = _apply(MarkerEdits(added=[], changed=[], removed=[_marker("businessPhones", False)]), tmp_path)

    assert '@odata(name="businessPhones")' in _text(tmp_path)
    assert "beta=" not in _text(tmp_path)
    assert [edit.action for edit in report.edits] == ["removed"]


def test_the_second_run_is_a_no_op(tmp_path):
    edits = MarkerEdits(added=[_marker("uid", True)], changed=[], removed=[])
    _apply(edits, tmp_path)

    again = apply_markers(edits, _tree(tmp_path), dry_run=False)

    assert again.edits == []
    assert again.is_empty


def test_a_dry_run_reports_without_writing(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("uid", True)], changed=[], removed=[]), tmp_path)
    before = _text(tmp_path)

    dry = apply_markers(
        MarkerEdits(added=[_marker("mentions", True)], changed=[], removed=[]), _tree(tmp_path), dry_run=True
    )

    assert not dry.is_empty
    assert _text(tmp_path) == before
    assert report.edits


def test_a_member_declared_on_a_base_class_is_marked_where_it_is_written(tmp_path):
    edits = MarkerEdits(added=[_marker("createdDateTime", True)], changed=[], removed=[])

    report = apply_markers(edits, _tree(tmp_path, widget=SOURCE, entity=BASE_SOURCE), dry_run=False)

    assert '@odata(name="createdDateTime", beta=True, readonly=True)' in _text(tmp_path, "entity")
    assert '@odata(name="uid")' in _text(tmp_path, "widget")
    assert report.edits[0].path.endswith("entity.py")


def test_a_member_no_decorator_declares_is_reported_not_guessed(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("notDeclaredAnywhere", True)], changed=[], removed=[]), tmp_path)

    assert report.edits == []
    assert report.skipped[0][1] == "no @odata(name=...) declares this member"
    assert "notDeclaredAnywhere" not in _text(tmp_path)


def test_a_method_marker_is_skipped_because_methods_are_not_generated(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("markAsJunk", True, "method")], changed=[], removed=[]), tmp_path)

    assert report.edits == []
    assert "generate_methods" in report.skipped[0][1]


def test_a_preview_member_that_went_stable_loses_its_marker(tmp_path):
    """The promotion case: the plan is empty, so the declared marker has to go."""
    _apply(MarkerEdits(added=[_marker("uid", True)], changed=[], removed=[]), tmp_path)
    assert "beta=True" in _text(tmp_path)

    declared = read_declared_markers({"microsoft.graph.Widget": tmp_path / "widget.py"})
    edits = compare_markers(MarkerPlan(base="v1", target="beta", markers=[]), declared)
    report = apply_markers(edits, _tree(tmp_path), dry_run=False)

    assert {marker.member for marker in edits.removed} == {"uid", "businessPhones"}
    assert "beta=" not in _text(tmp_path)
    assert {edit.action for edit in report.edits} == {"removed"}


def test_a_rename_the_preview_adopted_is_marked_as_a_rename(tmp_path):
    _apply(MarkerEdits(added=[], changed=[], removed=[]), tmp_path)
    plan = MarkerPlan(
        base="v1",
        target="beta",
        markers=[MemberMarker("microsoft.graph.Widget", "mentions", "navigation", "widgetMentions", RENAMED)],
    )

    edits = compare_markers(plan, read_declared_markers({"microsoft.graph.Widget": tmp_path / "widget.py"}))
    apply_markers(edits, _tree(tmp_path), dry_run=False)

    assert '@odata(name="mentions", beta="widgetMentions", navigation=True)' in _text(tmp_path)
    assert "beta=" in _text(tmp_path)


def _gate() -> MarkerEdits:
    return MarkerEdits(added=[], changed=[], removed=[], types_added=[VersionMarker("microsoft.graph.Widget", "beta")])


def test_a_type_only_the_preview_root_declares_states_its_version(tmp_path):
    """The class is where the version is knowable, so the class is where the fact is written."""
    report = _apply(_gate(), tmp_path)

    assert '@version("beta")\nclass Widget(Entity):\n' in _text(tmp_path)
    assert "from office365.runtime.types.odata_property import odata, version" in _text(tmp_path)
    assert [(edit.action, edit.member) for edit in report.edits] == [("added", "version")]
    assert read_declared_versions({"microsoft.graph.Widget": tmp_path / "widget.py"}) == {
        "microsoft.graph.Widget": frozenset({"beta"})
    }


def test_the_gate_is_written_once_even_when_the_run_repeats(tmp_path):
    _apply(_gate(), tmp_path)
    first = _text(tmp_path)

    report = _apply_again(_gate(), tmp_path)

    assert _text(tmp_path) == first
    assert report.edits == []


def test_a_gate_the_snapshots_stop_justifying_is_removed(tmp_path):
    _apply(_gate(), tmp_path)

    ungated = MarkerEdits(
        added=[], changed=[], removed=[], types_removed=[VersionMarker("microsoft.graph.Widget", "beta")]
    )
    report = _apply_again(ungated, tmp_path)

    assert "@version(" not in _text(tmp_path)
    assert "import odata\n" in _text(tmp_path)
    assert [(edit.action, edit.member) for edit in report.edits] == [("removed", "version")]


def test_a_value_type_is_not_gated_because_no_request_can_name_it(tmp_path):
    """A gate nothing enforces is a comment pretending to be a rule."""
    report = apply_markers(_gate(), _tree(tmp_path, widget=VALUE_SOURCE))

    assert "@version(" not in _text(tmp_path)
    assert "not addressed by a request" in report.skipped[0][1]


NO_DECLARATION_IMPORT = """from office365.entity import Entity


class Widget(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""


def test_the_import_is_written_for_a_class_that_declares_nothing_else(tmp_path):
    """A type with no properties imports no declaration module; the gate brings it in."""
    _apply(_gate(), tmp_path, widget=NO_DECLARATION_IMPORT)

    assert "from office365.entity import Entity\nfrom office365.runtime.types.odata_property import version\n" in _text(
        tmp_path
    )


def test_the_import_goes_back_out_with_the_last_gate(tmp_path):
    """An import nothing names is litter, so un-gating takes it back."""
    _apply(_gate(), tmp_path, widget=NO_DECLARATION_IMPORT)
    _apply_again(
        MarkerEdits(added=[], changed=[], removed=[], types_removed=[VersionMarker("microsoft.graph.Widget", "beta")]),
        tmp_path,
    )

    assert "odata_property" not in _text(tmp_path)
