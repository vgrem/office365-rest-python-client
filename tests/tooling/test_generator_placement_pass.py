"""The placement pass: where a module is allowed to live.

``--place`` is the only command that rewrites *where a class lives*, so what matters about it is
the rule, not the moves it happens to make: a stem may be shortened and nested, never lengthened,
and the real tree is where the rule has to hold today.
"""

from __future__ import annotations

from pathlib import Path

from generator.cli.session import GENERATOR_DIR, Session
from generator.tools.placement import plan_placement


def _module(path: Path, class_name: str) -> Path:
    """A module with one class named after the OData type, which is what the pass reads."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"class {class_name}:\n    pass\n", encoding="utf-8")
    return path


def _package(root: Path, *parts: str) -> Path:
    """A package path with the ``__init__.py`` files descent requires to walk into it."""
    directory = root.joinpath(*parts)
    directory.mkdir(parents=True, exist_ok=True)
    for parent in (directory, *directory.parents):
        if root in parent.parents:
            init = parent / "__init__.py"
            if not init.exists():
                init.write_text("", encoding="utf-8")
    return directory


def _tree(root: Path) -> None:
    _package(root, "pkg", "devices", "management")
    _package(root, "pkg", "devices", "compliance")


def _plan(root: Path):
    return plan_placement(root / "pkg", str(root), root)


def test_moves_a_module_into_the_package_that_claims_it(tmp_path: Path) -> None:
    _tree(tmp_path)
    _module(tmp_path / "pkg" / "devices" / "management_intent.py", "DeviceManagementIntent")

    plan = _plan(tmp_path)

    assert [move.new_path for move in plan.moves] == ["pkg/devices/management/intent.py"]
    assert plan.moves[0].new_module == "pkg.devices.management.intent"


def test_refuses_a_stem_the_derivation_would_lengthen(tmp_path: Path) -> None:
    """``devices/data.py`` is a decision; ``and_app_management_data.py`` is a regression."""
    _tree(tmp_path)
    _module(tmp_path / "pkg" / "devices" / "data.py", "DeviceAndAppManagementData")

    assert _plan(tmp_path).moves == []


def test_leaves_a_module_whose_class_is_not_its_whole_name(tmp_path: Path) -> None:
    """``migration/tasks.py`` is a table of task species; ``task.py`` would hide them."""
    _tree(tmp_path)
    path = tmp_path / "pkg" / "devices" / "management_tasks.py"
    path.write_text(
        'class DeviceManagementTask:\n    pass\n\n\nFILE_SHARE = "file"\n',
        encoding="utf-8",
    )

    plan = _plan(tmp_path)

    assert plan.moves == []
    assert plan.skipped == ["pkg/devices/management_tasks.py"]


def test_the_intune_tree_is_a_fixed_point() -> None:
    """The pass exists so this holds: no module sits above the package that claims it.

    Pinned on one product rather than the whole model, because the rest of the model has
    not been swept yet -- and a gate that fails for a directory nobody has touched yet
    would be turned off rather than satisfied.
    """
    options = Session.open("graph").options
    root = Path(options.output_path) / "intune"

    plan = plan_placement(root, options.output_path, GENERATOR_DIR.parent)

    assert plan.moves == [], plan.render()
