"""Place the modules a subpackage already claims, and move nothing else.

:func:`~generator.planning.routing.descend_module` answers where a *new* type's file
goes. Placement is sticky, so the question was never asked of the files already
written, and a tree grows one flat layer beside its own subpackages:
``devices/management_intent.py`` next to ``devices/management/intent.py``. Measured on
``office365/intune`` (754 modules), that flat layer is 89 files and 59 of them sit in a
package whose subdirectory already consumes their class name.

Two rules keep the pass honest:

* **only a move may shorten a stem.** An existing stem is a decision. A derivation that
  lengthens it -- ``compliance/device_status.py`` back to
  ``device_compliance_device_status.py``, ``devices/data.py`` to
  ``and_app_management_data.py`` -- is un-stripping what the parent package already says,
  and re-adding a prefix the directory makes redundant. Those stay where they are.
* **a move descends, never climbs.** So applying the plan to its own output terminates,
  strictly, and the result is a fixed point: a second ``--place`` proposes nothing.

Import rewriting is textual on purpose. A moved module is a *string* in every import
that names it, the tree keeps one class per module, and the token is unambiguous; an
AST round-trip would reformat the file it edited.
"""

from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Mapping, Optional

from generator.planning.routing import descend_module

#: Files whose text may name a moved module. Markdown counts: the docs and the examples
#: quote import paths, and a stale one is a broken example, not a stale comment.
TEXT_SUFFIXES = frozenset({".py", ".md", ".rst", ".txt", ".yaml", ".yml", ".cfg"})

#: Directories never scanned: the same ones the import sweep skips.
PRUNED = frozenset(
    {".git", ".venv", "__pycache__", "node_modules", "dist", "build", ".mypy_cache", ".ruff_cache", ".pytest_cache"}
)


@dataclass(frozen=True)
class PlacementMove:
    """One module that belongs to a subdirectory of the package it is in."""

    path: str
    new_path: str
    class_name: str

    @property
    def module(self) -> str:
        return module_of(self.path)

    @property
    def new_module(self) -> str:
        return module_of(self.new_path)

    @property
    def stem(self) -> str:
        return Path(self.path).stem

    @property
    def new_stem(self) -> str:
        return Path(self.new_path).stem

    def to_dict(self) -> dict:
        return {
            "file": self.path,
            "new_file": self.new_path,
            "type": self.class_name,
            "module": self.module,
            "new_module": self.new_module,
        }


@dataclass(frozen=True)
class PlacementPlan:
    """What one pass would move, and what it declined to read."""

    root: str
    moves: List[PlacementMove] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    #: Moves the descent wanted but the tree refused: the target file is taken by a
    #: module that defines the same class, which is a duplicate to review, not to merge.
    blocked: List[PlacementMove] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not self.moves

    def to_dict(self) -> dict:
        return {
            "root": self.root,
            "moves": [move.to_dict() for move in self.moves],
            "blocked": [move.to_dict() for move in self.blocked],
            "skipped": list(self.skipped),
        }

    def render(self, base: Optional[str] = None) -> str:
        """The plan as a report: one line per move, then the count that matters."""
        if not self.moves:
            return f"placement: {self.root} is a fixed point ({len(self.skipped)} module(s) unreadable)"
        lines = [
            f"  {_relative(move.path, base)}  ->  {_relative(move.new_path, base)}  [{move.class_name}]"
            for move in self.moves
        ]
        shortened = sum(1 for move in self.moves if move.stem != move.new_stem)
        lines.append(
            f"placement: {len(self.moves)} move(s) in {self.root} "
            f"({shortened} shortening a stem, {len(self.blocked)} blocked, {len(self.skipped)} module(s) unreadable)"
        )
        for move in self.blocked:
            pair = f"{_relative(move.path, base)}  ->  {_relative(move.new_path, base)}"
            lines.append(f"  blocked: {pair}  (target taken)")
        return "\n".join(lines)


def module_of(path: str) -> str:
    """``office365/a/b.py`` -> ``office365.a.b``."""
    return path.replace("\\", "/").removesuffix(".py").replace("/", ".")


def _relative(path: str, base: Optional[str]) -> str:
    if not base:
        return path
    try:
        return os.path.relpath(path, base)
    except ValueError:  # different drives on Windows
        return path


def _classes(path: Path) -> List[str]:
    """Top-level class names in a module -- what the tree keeps one of per file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return []
    return [node.name for node in tree.body if isinstance(node, ast.ClassDef)]


def plan_placement(root: Path | str, output_base: str, repo_root: Path | str) -> PlacementPlan:
    """Every module under ``root`` that ``descend_module`` would place deeper.

    ``root`` is the directory to sweep, ``output_base`` the router's output path
    (``.../office365``) because that is what turns a module back into a file, and
    ``repo_root`` what the report is written relative to.
    """
    base = Path(repo_root)
    moves: List[PlacementMove] = []
    blocked: List[PlacementMove] = []
    skipped: List[str] = []
    for path in sorted(Path(root).rglob("*.py")):
        if PRUNED & set(path.parts) or path.name == "__init__.py":
            continue
        relative = path.relative_to(base).as_posix() if base in path.parents else str(path)
        classes = _classes(path)
        if len(classes) != 1:
            skipped.append(relative)
            continue
        class_name = classes[0]
        package, _, stem = module_of(relative).rpartition(".")
        module_path, new_stem = descend_module(package, class_name, str(output_base))
        new_path = f"{module_path}.{new_stem}".replace(".", "/") + ".py"
        if new_path == relative:
            continue
        # A move may shorten a stem and nest it; it may not lengthen one. Lengthening
        # re-adds the prefix the parent package already says (`data.py`,
        # `device_status.py`), which is the derivation arguing with the tree.
        if len(new_stem) > len(stem) or (Path(new_path).parent == Path(relative).parent and new_stem == stem):
            continue
        move = PlacementMove(path=relative, new_path=new_path, class_name=class_name)
        if (base / new_path).exists():
            blocked.append(move)
        else:
            moves.append(move)
    return PlacementPlan(root=_relative(str(Path(root)), str(base)), moves=moves, skipped=skipped, blocked=blocked)


def rewrite_imports(
    renames: Mapping[str, str], repo_root: Path | str, *, suffixes: Iterable[str] = TEXT_SUFFIXES
) -> List[str]:
    """Rewrite every mention of a moved module in the tree; returns the edited files.

    One pass, longest module first, so ``a.b.c`` is never matched as ``a.b`` plus a
    trailing token -- and only whole tokens, so a module that is a prefix of another
    (``...devices.data`` vs ``...devices.database``) cannot be clipped.
    """
    if not renames:
        return []
    base = Path(repo_root)
    ordered = sorted(renames.items(), key=lambda item: len(item[0]), reverse=True)
    pattern = re.compile("(?<![\\w.])(%s)(?![\\w])" % "|".join(re.escape(old) for old, _ in ordered))
    lookup = dict(ordered)
    edited: List[str] = []
    for path in sorted(base.rglob("*")):
        if not path.is_file() or path.suffix not in suffixes or PRUNED & set(path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        replaced, count = pattern.subn(lambda match: lookup[match.group(1)], text)
        if count:
            path.write_text(replaced, encoding="utf-8")
            edited.append(path.relative_to(base).as_posix())
    return edited


def _move(path: Path, new_path: Path, repo_root: Path) -> None:
    """``git mv`` when the tree is a repository, so the rename stays a rename."""
    new_path.parent.mkdir(parents=True, exist_ok=True)
    if new_path.exists():
        raise FileExistsError(f"placement would overwrite {new_path}")
    if (repo_root / ".git").exists():
        result = subprocess.run(
            ["git", "mv", str(path), str(new_path)], cwd=str(repo_root), capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            return
    shutil.move(str(path), str(new_path))


def apply_placement(plan: PlacementPlan, repo_root: Path | str, *, rewrite: bool = True) -> List[str]:
    """Move the plan's files, then the imports that name them."""
    base = Path(repo_root)
    moved: List[str] = []
    for move in plan.moves:
        _move(base / move.path, base / move.new_path, base)
        moved.append(move.new_path)
    if rewrite:
        rewrite_imports({move.module: move.new_module for move in plan.moves}, base)
    return moved


def write_report(plan: PlacementPlan, path: str) -> None:
    Path(path).write_text(json.dumps(plan.to_dict(), indent=2) + "\n", encoding="utf-8")


def place(
    root: Path | str,
    output_base: str,
    repo_root: Path | str,
    *,
    apply: bool = False,
    limit: int = 8,
) -> PlacementPlan:
    """Plan, then (with ``apply``) move, until the tree stops changing.

    A single pass cannot reach the fixed point: moving a file out of a directory can free
    the stem its neighbour wanted, so the neighbour becomes movable one pass later. Each
    pass descends, so the loop is bounded by the tree's depth -- ``limit`` guards against a
    rule that stops obeying that; it is not a tuning knob.
    """
    root_path = Path(root)
    moves: List[PlacementMove] = []
    blocked: List[PlacementMove] = []
    skipped: List[str] = []
    for _ in range(limit if apply else 1):
        plan = plan_placement(root_path, output_base, repo_root)
        moves.extend(plan.moves)
        blocked, skipped = plan.blocked, plan.skipped
        if plan.is_empty() or not apply:
            break
        apply_placement(plan, repo_root)
    return PlacementPlan(root=_relative(str(root_path), str(repo_root)), moves=moves, skipped=skipped, blocked=blocked)


__all__ = [
    "PlacementMove",
    "PlacementPlan",
    "apply_placement",
    "module_of",
    "place",
    "plan_placement",
    "rewrite_imports",
    "write_report",
]
