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
(``singleValueExtendedProperties``, ``attachments``, ``masterCategories``, ...) —
and one that names a column the metadata has never heard of, which says
``system=True`` instead (a list item's ``AuthorId``, a page's ``FileLeafRef``:
the CSDL describes the object graph, not the item row).

A member the service assigns rather than the client is finished the same way, with
``readonly=True`` (CSDL ``Org.OData.Core.V1.Computed``: ``createdDateTime``,
``id`` on some types, every ``lastModifiedDateTime``). The fact lives on a
schema-level ``<Annotations Target="Type/member">`` block, never on the property
element, so it is read out of the document and carried per member here.

A member the preview surface alone declares is finished with ``beta=True``, and it is
read the same way -- ``Com.Microsoft.VisualStudio.CodeGen.IsBeta`` on the same kind of
block. Who states it depends on how the service states its preview. Where the two
surfaces are two snapshots (Graph), a preview *type* carries an ``@version("beta")`` gate
and its members need no mark: the class owns that fact (962 of SharePoint's 1,401 member
annotations sit inside a preview type). Where they are one document (SharePoint), there
is no gate to write -- ``@version`` names a service root and SharePoint has one -- so the
member keeps the mark and the fact survives in the tree at its declaration.

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
import functools
import pathlib
import sys
from typing import Dict, List, NamedTuple, Optional, Set

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from generator.config import GeneratorOptions  # noqa: E402
from generator.intrinsic_members import intrinsic_members  # noqa: E402
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

#: Service -> the preview root's snapshot, read when it sits next to the stable one.
#: ``system=True`` claims the metadata has never heard of a name, and a member that only
#: the preview declares (``Event.uid``) is heard of: answering ``system`` for it would
#: say the column is invented by the client when it is a documented preview member.
#: Graph has a ``/beta`` root; SharePoint has one v3 document, and naming the Graph file
#: for it as well handed the v3 reader a document no type could be read out of.
_PREVIEW_SNAPSHOT = {"graph": "GraphBeta.xml"}


class Declared(NamedTuple):
    """A CSDL property: its OData name, whether $expand reaches it, and its kind."""

    name: str
    navigation: bool
    enum: bool
    readonly: bool = False
    #: The type's own CSDL is silent and every one of its subtypes states it, so the
    #: column exists on every instance (see :mod:`generator.intrinsic_members`).
    system: bool = False
    #: Only the preview surface declares the member (CSDL ``...CodeGen.IsBeta``). A member
    #: of a preview type keeps the mark only where the *type* cannot state it: see
    #: :func:`_catalog_of`.
    beta: bool = False


#: CSDL type name (lowercased) -> {OData name: declaration}
Catalog = Dict[str, Dict[str, Declared]]


class Edit(NamedTuple):
    """One source change: insert ``new`` before ``lineno``, or replace ``old`` with it."""

    lineno: int
    old: Optional[str]
    new: str


Edits = List[Edit]


@functools.lru_cache(maxsize=None)
def load_catalog(service: str) -> Catalog:
    """Map each CSDL type name to the properties it has, its base types included.

    A CSDL type declares what it *adds*: ``onlineMeeting`` has no ``joinInformation``,
    its base ``onlineMeetingBase`` has. Answering from the type's own node alone would
    read that member as one the metadata has never heard of -- which is exactly what
    ``system=True`` claims -- and would hide every inherited column from the back-fill.
    So the base chain is folded in here, once, nearest declaration winning.
    """
    source, reader = _SERVICES[service]
    options = GeneratorOptions.load(source, _GENERATOR_DIR)
    model = reader(options.metadata_path).read()
    # A service whose two surfaces are two snapshots gates the preview on the class, and a
    # class that states it owns it for all its members. A service that ships one document
    # has no such gate to write, so the member has to say it.
    two_roots = service in _PREVIEW_SNAPSHOT
    catalog = _catalog_of(model, two_roots=two_roots)
    bases = _bases_of(model)
    preview_name = _PREVIEW_SNAPSHOT.get(service)
    preview = pathlib.Path(options.metadata_path).parent / preview_name if preview_name else None
    if preview is not None and preview.is_file():
        model = reader(str(preview)).read()
        for name, properties in _catalog_of(model, two_roots=True).items():
            declared = catalog.setdefault(name, {})
            for prop, declaration in properties.items():
                known = declared.get(prop)
                if known is None:
                    declared[prop] = declaration
                elif declaration.readonly and not known.readonly:
                    # Ownership is a fact of the service: a member the preview already
                    # reports as computed is computed under either root.
                    declared[prop] = known._replace(readonly=True)
        bases.update(_bases_of(model))
    return {name: _inherited(name, catalog, bases) for name in catalog}


def _bases_of(model) -> Dict[str, str]:
    """CSDL type name (lowercased) -> the type it derives from, if any."""
    return {name.lower(): (schema.BaseTypeName or "").lower() for name, schema in model.types.items()}


def _inherited(name: str, own: Catalog, bases: Dict[str, str]) -> Dict[str, Declared]:
    """One type's declarations with its base chain folded in.

    Nearest declaration wins, so a type that narrows a member it inherits keeps its own
    answer. A chain that loops is cut rather than followed: the snapshot is data.
    """
    properties: Dict[str, Declared] = {}
    seen: Set[str] = set()
    current = name
    while current and current not in seen:
        seen.add(current)
        for prop, declaration in own.get(current, {}).items():
            properties.setdefault(prop, declaration)
        current = bases.get(current, "")
    return properties


def _catalog_of(model, *, two_roots: bool = True) -> Catalog:
    """The declarations one snapshot carries, type name lowercased.

    ``two_roots`` decides who states a member's previewness. Where the surfaces are two
    snapshots (Graph), the type carries an ``@version("beta")`` gate and repeating it on
    1,401 members would be one fact with two owners -- measured over SharePoint's document.
    Where they are one document (SharePoint), there is no gate to write: ``@version`` names
    a service root, SharePoint has one, and a marker that says otherwise makes an *offline*
    hydration of the type refuse (`offline_context()` is a `GraphClient`). So there the
    member states it, and the fact survives in the tree at its declaration.
    """

    def is_enum(type_name: str) -> bool:
        bare = type_name[len("Collection(") : -1] if type_name.startswith("Collection(") else type_name
        declared = model.types.get(bare)
        return declared is not None and declared.BaseTypeFullName == "EnumType"

    intrinsic = intrinsic_members(model)
    catalog: Catalog = {}
    for name, schema in model.types.items():
        properties = {
            prop.Name: Declared(
                prop.Name,
                bool(prop.IsNavigation),
                is_enum(prop.TypeName or ""),
                bool(prop.ReadOnly),
                beta=bool(prop.IsBeta) and not (two_roots and schema.IsBeta),
            )
            for prop in schema.Properties.values()
        }
        catalog[name.lower()] = properties
        # A promoted member is not declared by this type, so it is not in the loop above:
        # it is the subtypes' declaration, which is what ``system=True`` says.
        for prop in intrinsic.get(name, ()):
            properties.setdefault(prop.Name, Declared(prop.Name, bool(prop.IsNavigation), False, False, True))
    return catalog


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


def declared_of(properties: Dict[str, Declared], name: str) -> Optional[Declared]:
    """The member a name refers to, spelling case aside, or ``None``.

    The snapshot spells one member differently on different types -- ``drive`` declares
    ``sharePointIds``, ``driveItem`` declares ``sharepointIds``; ``sitePage`` declares
    ``webParts``, ``verticalSection`` declares ``webparts``. A getter that reads another
    type's spelling still names a member the metadata declares, so it is not a ``system``
    column: the flag says the metadata is silent, which is a fact about the member, not
    about the bytes we happened to type.
    """
    if not name:
        return None
    declared = properties.get(name)
    if declared is not None:
        return declared
    key = name.lower()
    return next((found for spelling, found in properties.items() if spelling.lower() == key), None)


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


def marker_edit(call: ast.Call, keywords: List[str], source_line: str) -> Optional[Edit]:
    """Add ``keyword=True`` for each of ``keywords`` the marker lacks, on one line.

    One edit, not one per keyword: two edits on the same line cannot both write it,
    and a declaration that is missing two facts is still one declaration.
    """
    missing = [keyword for keyword in keywords if not any(k.arg == keyword for k in call.keywords)]
    if not missing:
        return None
    if call.end_lineno != call.lineno:  # a wrapped declaration: leave it to a human
        return None
    stripped = source_line.rstrip("\n")
    if not stripped.endswith(")"):
        return None
    added = "".join(f", {keyword}=True" for keyword in missing)
    return Edit(call.lineno, source_line, stripped[:-1] + added + ")\n")


def pending_markers(
    tree: ast.Module,
    class_node: ast.ClassDef,
    properties: Dict[str, Declared],
    lines: List[str],
    *,
    only: Optional[Set[str]] = None,
    duplicates: Optional[List[str]] = None,
) -> Edits:
    """The declarations a class still needs, and the markers that need finishing.

    ``only`` finishes those facts and nothing else, and adds no declaration: declaring
    a name changes what a property holds (an enum-typed one starts answering a member),
    so the back-fill is its own decision, and one fact can land without it.

    ``duplicates`` collects the getters given no declaration because a getter of the
    same class already answers for that wire name -- one fact, one owner. Two
    declarations of one name leave the class holding both getters but
    ``_schema.properties[name].attr`` pointing at whichever came last, so
    ``get_property("guestSettings")`` would answer a ``TeamMessagingSettings``.
    """
    claimed: Dict[str, str] = {}
    for node in class_node.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        existing = declaration(node)
        owner = declared_name(existing) if existing is not None else None
        if owner:
            claimed.setdefault(owner, node.name)
    markers = []
    for node in class_node.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if not any(getattr(d, "id", "") == "property" for d in node.decorator_list if not isinstance(d, ast.Call)):
            continue
        existing = declaration(node)
        if existing is not None:
            name = declared_name(existing) or ""
            declared = properties.get(name)
            if declared is None:
                # A member this type spells otherwise (``sharepointIds`` beside
                # ``sharePointIds``) is declared, so it is not a ``system`` column, and
                # the facts of that member do not belong on this spelling: nothing to do
                # but leave the declaration to whoever fixes the name.
                wanted = [] if declared_of(properties, name) is not None else ["system"]
            else:
                wanted = [
                    keyword
                    for keyword, declared_by in (
                        ("navigation", declared.navigation),
                        ("readonly", declared.readonly),
                        ("system", declared.system),
                        ("beta", declared.beta),
                    )
                    if declared_by
                ]
            finishes = [keyword for keyword in wanted if only is None or keyword in only]
            edit = marker_edit(existing, finishes, lines[existing.lineno - 1]) if finishes else None
            if edit is not None:
                markers.append(edit)
            continue
        if only is not None:
            continue
        names = read_spelled_names(node)
        if len(names) != 1:
            continue  # a business method, or a getter that reads no single property
        name = names.pop()
        owner = claimed.get(name)
        if owner is not None:
            if duplicates is not None:
                duplicates.append(f"{class_node.name}.{node.name} reads {name!r}, declared by {owner}")
            continue
        claimed[name] = node.name
        declared = properties.get(name)
        if declared is None:
            # A client-side convenience, or this type's member under the spelling another
            # type uses (``sharepointIds`` beside ``sharePointIds``). Either way there is
            # no declaration to write: the codemod names a column only as the metadata
            # spells it, and this getter reads a name this type does not carry.
            continue
        suffix = "".join(
            f", {keyword}=True"
            for keyword, wanted in (
                ("navigation", declared.navigation),
                ("readonly", declared.readonly),
                ("system", declared.system),
                ("beta", declared.beta),
            )
            if wanted
        )
        marker = f'    @odata(name="{name}"{suffix})\n'
        markers.append(Edit(node.decorator_list[0].lineno, None, marker))
    return markers


def plan_module(
    path: pathlib.Path,
    catalog: Catalog,
    index: Dict[str, Dict[str, Declared]],
    *,
    only: Optional[Set[str]] = None,
    duplicates: Optional[List[str]] = None,
) -> Edits:
    """The line insertions one module needs, without touching it."""
    source = path.read_text(encoding="utf-8")
    if "@property" not in source:
        return []
    tree = ast.parse(source)
    found = subject(tree, catalog, index)
    if found is None:
        return []
    markers = pending_markers(
        tree, found.node, found.properties, source.splitlines(keepends=True), only=only, duplicates=duplicates
    )
    if not markers or _imports_odata(tree):
        return markers
    last_import = max(
        node.end_lineno or node.lineno
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        and not (isinstance(node, ast.ImportFrom) and node.module == "__future__")
    )
    return markers + [Edit(last_import + 1, None, _ODATA_IMPORT + "\n")]


def _imports_odata(tree: ast.Module) -> bool:
    """Whether the module already imports ``odata``, however it spells the import line."""
    return any(
        isinstance(node, ast.ImportFrom)
        and node.module == "office365.runtime.types.odata_property"
        and any(alias.name == "odata" for alias in node.names)
        for node in tree.body
    )


def mark_module(
    path: pathlib.Path,
    catalog: Catalog,
    index: Dict[str, Dict[str, Declared]],
    *,
    only: Optional[Set[str]] = None,
    duplicates: Optional[List[str]] = None,
) -> int:
    """Apply the planned declarations to one module; return how many were applied."""
    markers = plan_module(path, catalog, index, only=only, duplicates=duplicates)
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
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("root", help="package directory to update, e.g. office365/outlook")
    parser.add_argument("--service", choices=sorted(_SERVICES), default="graph", help="which CSDL to read")
    parser.add_argument("--dry-run", action="store_true", help="report the diff size without writing")
    parser.add_argument(
        "--only",
        action="append",
        metavar="FACT",
        help="finish only this fact (navigation, readonly, system, beta), and add no declaration",
    )
    args = parser.parse_args(argv)

    catalog = load_catalog(args.service)
    index = type_index(catalog)
    files = markers = 0
    for path in sorted(pathlib.Path(args.root).rglob("*.py")):
        only = set(args.only) if args.only else None
        duplicates: List[str] = []
        planned = plan_module(path, catalog, index, only=only, duplicates=duplicates) if args.dry_run else None
        added = (
            len(planned) if planned is not None else mark_module(path, catalog, index, only=only, duplicates=duplicates)
        )
        for duplicate in duplicates:
            print(f"{path}: {duplicate}", file=sys.stderr)
        if added:
            files += 1
            markers += added
            if args.dry_run:
                print(f"{path}: {added}")
    print(f"{'would mark' if args.dry_run else 'marked'}: {markers} lines in {files} modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
