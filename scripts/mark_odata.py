"""Declare its OData name on every generated getter (one-time codemod).

The generator now emits ``@odata(name=..., navigation=True)`` with each getter, but
it only renders *missing* members, so files generated before that change stay
unmarked until they happen to gain a property. This script closes the gap: it reads
the name each getter already queries (``self.properties.get("iCalUId", ...)``) and,
when the service metadata confirms that name belongs to the file's own type,
declares it above the existing ``@property``.

It also finishes a declaration that is already there but incomplete — a name
without ``navigation=True`` where the CSDL says ``NavigationProperty``, which is
how the first pass left every file that was already marked
(``singleValueExtendedProperties``, ``attachments``, ``masterCategories``, ...).

The OData name is never derived from the attribute name: ``iCalUId`` and ``icalUid``
both survive a snake-case round trip, and only one of them is a real column. The
literal in the getter is the ground truth; the metadata only vouches for it and
supplies the navigation flag.

Declaring an enum-typed property changes the value the object holds: generated Graph
enums spell their CSDL ordinal (``EventType.singleInstance = "0"``) while the service
sends the member *name*, so a reader that compared ``type`` to ``"seriesMaster"`` now
receives a member. Read such a property through ``.name`` (or the declaration) instead.

Usage::

    uv run python scripts/mark_odata.py office365/outlook --dry-run
    uv run python scripts/mark_odata.py office365/outlook
    uv run ruff check --fix office365/outlook   # sort the new import
"""

from __future__ import annotations

import argparse
import ast
import pathlib
import sys
from typing import Dict, List, NamedTuple, Optional, Set

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from generator.config import GeneratorOptions  # noqa: E402
from generator.odata.v3.metadata_reader import ODataV3Reader  # noqa: E402
from generator.odata.v4.metadata_reader import ODataV4Reader  # noqa: E402

_ODATA_IMPORT = "from office365.runtime.types.odata_property import odata"
_GENERATOR_DIR = pathlib.Path(__file__).resolve().parents[1] / "generator"

#: Service -> (metadata source, reader). A Graph module names its own
#: type; a generated SharePoint module does not — the class name is the only handle
#: back, which :func:`type_index` inverts from the CSDL last segment.
_SERVICES = {
    "graph": ("graph", ODataV4Reader),
    "sharepoint": ("sharepoint", ODataV3Reader),
}


class Declared(NamedTuple):
    """A CSDL property: its OData name, whether $expand reaches it, and its kind."""

    name: str
    navigation: bool
    enum: bool


#: CSDL type name (lowercased) -> {OData name: declaration}
Catalog = Dict[str, Dict[str, Declared]]


class Edit(NamedTuple):
    """One source change: insert ``new`` before ``lineno``, or replace ``old`` with it."""

    lineno: int
    old: Optional[str]
    new: str


Edits = List[Edit]


def load_catalog(service: str) -> Catalog:
    """Map each CSDL type name to the properties it declares itself."""
    source, reader = _SERVICES[service]
    options = GeneratorOptions.load(source, _GENERATOR_DIR)
    model = reader(options.metadata_path).read()

    def is_enum(type_name: str) -> bool:
        bare = type_name[len("Collection(") : -1] if type_name.startswith("Collection(") else type_name
        declared = model.types.get(bare)
        return declared is not None and declared.BaseTypeFullName == "EnumType"

    return {
        name.lower(): {
            prop.Name: Declared(prop.Name, bool(prop.IsNavigation), is_enum(prop.TypeName or ""))
            for prop in schema.Properties.values()
        }
        for name, schema in model.types.items()
    }


def declared_type_name(tree: ast.Module, catalog: Catalog) -> Optional[str]:
    """The CSDL type name the module's ``entity_type_name`` returns.

    The module is asked first, because it is the one place that can name a type outright
    -- and it sometimes spells the CSOM name (``Microsoft.SharePoint.Administration...``)
    rather than the ``SP.`` alias, which is the same type under the name the metadata
    itself uses. So the catalog decides: a name it does not contain is not a type.
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name != "entity_type_name":
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and isinstance(child.value, ast.Constant):
                value = child.value.value
                if isinstance(value, str) and value.lower() in catalog:
                    return value
    return None


class Subject(NamedTuple):
    """The one class of a module whose CSDL type is known."""

    node: ast.ClassDef
    properties: Dict[str, Declared]


def subject(tree: ast.Module, catalog: Catalog, index: Dict[str, Dict[str, Declared]]) -> Optional[Subject]:
    """The module class whose CSDL type is known — never a guess.

    A module may name its own type (``entity_type_name``); failing that, its class name
    is matched against the CSDL last segment. Two candidates on either path is a guess.
    """
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    name = declared_type_name(tree, catalog)
    if name:
        properties = catalog.get(name.lower())
        return Subject(classes[0], properties) if properties and len(classes) == 1 else None
    matches = [node for node in classes if node.name.lower() in index]
    return Subject(matches[0], index[matches[0].name.lower()]) if len(matches) == 1 else None


def type_index(catalog: Catalog) -> Dict[str, Dict[str, Declared]]:
    """Lowercased class name -> declared properties, for modules that name no CSDL type.

    A generated SharePoint module usually spells its type name (``entity_type_name``),
    but the older ones do not: the CSDL does, and the module only carries the class. The
    generator turns a type's last segment into that class name, so the same rule inverts
    it — and a last segment two types share is dropped rather than guessed.
    """
    owners: Dict[str, List[str]] = {}
    for full_name in catalog:
        owners.setdefault(full_name.rsplit(".", 1)[-1], []).append(full_name)
    return {last: catalog[names[0]] for last, names in owners.items() if len(names) == 1}


def read_spelled_names(getter: ast.FunctionDef) -> Set[str]:
    """String literals the getter passes to ``properties.get``/``setdefault``."""
    names = set()
    for node in ast.walk(getter):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr not in {"get", "setdefault"} or not node.args:
            continue
        owner = node.func.value
        if isinstance(owner, ast.Attribute) and owner.attr == "properties":
            first = node.args[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                names.add(first.value)
    return names


def declaration(getter: ast.FunctionDef) -> Optional[ast.Call]:
    """The ``@odata(...)`` call the getter already carries, if any."""
    for decorator in getter.decorator_list:
        if isinstance(decorator, ast.Call) and getattr(decorator.func, "id", "") == "odata":
            return decorator
    return None


def declared_name(call: ast.Call) -> Optional[str]:
    """The ``name=`` argument of an ``@odata`` call."""
    for keyword in call.keywords:
        if keyword.arg == "name" and isinstance(keyword.value, ast.Constant):
            return str(keyword.value.value)
    return None


def navigation_edit(call: ast.Call, properties: Dict[str, Declared], source_line: str) -> Optional[Edit]:
    """Add ``navigation=True`` to a marker that names a ``NavigationProperty``."""
    declared = properties.get(declared_name(call) or "")
    if declared is None or not declared.navigation:
        return None
    if any(keyword.arg == "navigation" for keyword in call.keywords):
        return None
    if call.end_lineno != call.lineno:  # a wrapped declaration: leave it to a human
        return None
    stripped = source_line.rstrip("\n")
    if not stripped.endswith(")"):
        return None
    return Edit(call.lineno, source_line, stripped[:-1] + ", navigation=True)\n")


def pending_markers(
    tree: ast.Module, class_node: ast.ClassDef, properties: Dict[str, Declared], lines: List[str]
) -> Edits:
    """The declarations a class still needs, and the markers that need finishing."""
    markers = []
    for node in class_node.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if not any(getattr(d, "id", "") == "property" for d in node.decorator_list if not isinstance(d, ast.Call)):
            continue
        existing = declaration(node)
        if existing is not None:
            edit = navigation_edit(existing, properties, lines[existing.lineno - 1])
            if edit is not None:
                markers.append(edit)
            continue
        names = read_spelled_names(node)
        if len(names) != 1:
            continue  # a business method, or a getter that reads no single property
        name = names.pop()
        declared = properties.get(name)
        if declared is None:
            continue  # a client-side convenience, not a column of this type
        suffix = ", navigation=True" if declared.navigation else ""
        marker = f'    @odata(name="{name}"{suffix})\n'
        markers.append(Edit(node.decorator_list[0].lineno, None, marker))
    return markers


def plan_module(path: pathlib.Path, catalog: Catalog, index: Dict[str, Dict[str, Declared]]) -> Edits:
    """The line insertions one module needs, without touching it."""
    source = path.read_text(encoding="utf-8")
    if "@property" not in source:
        return []
    tree = ast.parse(source)
    found = subject(tree, catalog, index)
    if found is None:
        return []
    markers = pending_markers(tree, found.node, found.properties, source.splitlines(keepends=True))
    if not markers or _ODATA_IMPORT in source:
        return markers
    last_import = max(
        node.end_lineno or node.lineno
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        and not (isinstance(node, ast.ImportFrom) and node.module == "__future__")
    )
    return markers + [Edit(last_import + 1, None, _ODATA_IMPORT + "\n")]


def mark_module(path: pathlib.Path, catalog: Catalog, index: Dict[str, Dict[str, Declared]]) -> int:
    """Apply the planned declarations to one module; return how many were applied."""
    markers = plan_module(path, catalog, index)
    if not markers:
        return 0
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    for edit in sorted(markers, key=lambda e: e.lineno, reverse=True):
        if edit.old is None:
            lines.insert(edit.lineno - 1, edit.new)
            continue
        assert lines[edit.lineno - 1] == edit.old, f"{path}:{edit.lineno} moved under the plan"
        lines[edit.lineno - 1] = edit.new
    path.write_text("".join(lines), encoding="utf-8")
    return len(markers)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", help="package directory to update, e.g. office365/outlook")
    parser.add_argument("--service", choices=sorted(_SERVICES), default="graph", help="which CSDL to read")
    parser.add_argument("--dry-run", action="store_true", help="report the diff size without writing")
    args = parser.parse_args(argv)

    catalog = load_catalog(args.service)
    index = type_index(catalog)
    files = markers = 0
    for path in sorted(pathlib.Path(args.root).rglob("*.py")):
        planned = plan_module(path, catalog, index) if args.dry_run else None
        added = len(planned) if planned is not None else mark_module(path, catalog, index)
        if added:
            files += 1
            markers += added
            if args.dry_run:
                print(f"{path}: {added}")
    print(f"{'would mark' if args.dry_run else 'marked'}: {markers} lines in {files} modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
