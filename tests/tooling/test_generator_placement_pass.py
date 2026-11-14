"""The placement pass: what it moves, what it refuses, and when it stops.

``--place`` is the only command that rewrites *where a class lives*, so the tests are
about its two rules rather than about the output tree: a move may nest a module and
shorten its stem, it may never lengthen one, it may never land on a file, and a second
run must propose nothing. The last test pins the invariant on the real tree -- that is
the point of the pass, and the reason it exists as a test at all.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from generator.cli.session import GENERATOR_DIR, Session
from generator.tools.placement import (
    PlacementPlan,
    apply_placement,
    place,
    plan_placement,
    rewrite_imports,
)


def _module(path: Path, class_name: str, body: str = "") -> Path:
    """A module with one class named after the OData type, which is what the pass reads."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"class {class_name}:\n    pass\n" + textwrap.dedent(body), encoding="utf-8")
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


def _plan(root: Path) -> PlacementPlan:
    return plan_placement(root / "pkg", str(root), root)


def test_moves_a_module_into_the_package_that_claims_it(tmp_path: Path) -> None:
    _tree(tmp_path)
    _module(tmp_path / "pkg" / "devices" / "management_intent.py", "DeviceManagementIntent")

    plan = _plan(tmp_path)

    assert [move.new_path for move in plan.moves] == ["pkg/devices/management/intent.py"]
    assert plan.moves[0].module == "pkg.devices.management_intent"
    assert plan.moves[0].new_module == "pkg.devices.management.intent"


def test_leaves_a_module_the_tree_does_not_claim(tmp_path: Path) -> None:
    _tree(tmp_path)
    _module(tmp_path / "pkg" / "devices" / "windows_feature_update_profile.py", "WindowsFeatureUpdateProfile")

    assert _plan(tmp_path).moves == []


def test_refuses_a_stem_the_derivation_would_lengthen(tmp_path: Path) -> None:
    """``devices/data.py`` is a decision; ``and_app_management_data.py`` is a regression."""
    _tree(tmp_path)
    _module(tmp_path / "pkg" / "devices" / "data.py", "DeviceAndAppManagementData")

    assert _plan(tmp_path).moves == []


def test_refuses_to_land_on_an_existing_file(tmp_path: Path) -> None:
    _tree(tmp_path)
    _module(tmp_path / "pkg" / "devices" / "management_intent.py", "DeviceManagementIntent")
    _module(tmp_path / "pkg" / "devices" / "management" / "intent.py", "DeviceManagementIntent")

    plan = _plan(tmp_path)

    assert plan.moves == []
    assert [move.new_path for move in plan.blocked] == ["pkg/devices/management/intent.py"]


def test_reports_a_module_it_cannot_read(tmp_path: Path) -> None:
    _tree(tmp_path)
    (tmp_path / "pkg" / "devices" / "broken.py").write_text("class (:\n", encoding="utf-8")

    assert _plan(tmp_path).skipped == ["pkg/devices/broken.py"]


def test_apply_moves_the_file_and_renames_its_importers(tmp_path: Path) -> None:
    _tree(tmp_path)
    _module(tmp_path / "pkg" / "devices" / "management_intent.py", "DeviceManagementIntent")
    importer = tmp_path / "pkg" / "devices" / "management.py"
    importer.write_text("from pkg.devices.management_intent import DeviceManagementIntent\n", encoding="utf-8")

    apply_placement(_plan(tmp_path), tmp_path)

    assert (tmp_path / "pkg" / "devices" / "management" / "intent.py").is_file()
    assert not (tmp_path / "pkg" / "devices" / "management_intent.py").exists()
    assert importer.read_text(encoding="utf-8") == ("from pkg.devices.management.intent import DeviceManagementIntent\n")


def test_rewrite_imports_matches_whole_tokens_only(tmp_path: Path) -> None:
    """A moved module may be a prefix of another one; clipping it would corrupt the import."""
    source = tmp_path / "pkg" / "module.py"
    source.parent.mkdir(parents=True)
    source.write_text(
        "from pkg.devices.data import A\nfrom pkg.devices.database import B\nfrom pkg.devices.data_loader import C\n",
        encoding="utf-8",
    )

    rewrite_imports({"pkg.devices.data": "pkg.devices.management.data"}, tmp_path)

    assert source.read_text(encoding="utf-8") == (
        "from pkg.devices.management.data import A\n"
        "from pkg.devices.database import B\n"
        "from pkg.devices.data_loader import C\n"
    )


def test_the_pass_stops_at_a_fixed_point(tmp_path: Path) -> None:
    _tree(tmp_path)
    _module(tmp_path / "pkg" / "devices" / "management_intent.py", "DeviceManagementIntent")

    first = place(tmp_path / "pkg", str(tmp_path), tmp_path, apply=True)
    second = place(tmp_path / "pkg", str(tmp_path), tmp_path, apply=True)

    assert [move.new_path for move in first.moves] == ["pkg/devices/management/intent.py"]
    assert second.is_empty()
    assert (tmp_path / "pkg" / "devices" / "management" / "intent.py").is_file()


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
