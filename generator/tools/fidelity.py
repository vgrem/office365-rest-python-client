"""What the model declares, measured against what its service metadata declares.

Read from the source, not from the imported tree. The question -- does this class state
this column, and with which markers -- is answered by the decorator, so it is answered
of 2,700 modules as text in seconds where importing them to ask a class takes minutes
(and import order, and an environment that resolves every optional dependency).

Four answers, because four things can be true of a member the service declares:
absent from the model (:data:`MISSING`), held as a field that states no declaration
(:data:`UNDECLARED` -- it serializes under its own spelling, and nothing else about it
can be said), declared under a name the metadata does not declare (:data:`EXTRA`), and
declared without a marker the metadata carries (:data:`BETA`, :data:`READONLY`).

A gap the generator's own filters caused is not a gap: a member listed in
``ignored_properties``, or typed as an ``ignored_types`` name, is skipped silently. The
one that remains is a member the metadata declares and nothing in the configuration
accounts for, which is the only kind this report is about.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Tuple

from generator.core.config import split_ignored
from generator.odata.model import ODataModel

#: The service declares a column the model does not.
MISSING = "missing"
#: The model holds the field but states no ``@odata`` declaration for it.
UNDECLARED = "undeclared"
#: The model declares a name the service does not.
EXTRA = "extra"
#: The service's base type is a model class this class does not derive from.
BASE = "base"
#: The metadata marks the member preview and the declaration does not.
BETA = "beta"
#: The metadata marks the member service-assigned and the declaration does not.
READONLY = "readonly"
#: The member is one the generator's own filters skip -- accounted for, not a gap.
IGNORED = "ignored"

KINDS = (MISSING, UNDECLARED, EXTRA, BASE, BETA, READONLY, IGNORED)
#: The kinds a model is expected to have none of. :data:`IGNORED` is the opposite: the
#: report lists it so a member the configuration drops is seen, not silently absent.
GAPS = (MISSING, UNDECLARED, EXTRA, BASE, BETA, READONLY)

_WHAT = {
    MISSING: "a column the service declares, absent from the model",
    UNDECLARED: "a field the model holds, with no declaration of its own",
    EXTRA: "a name the model declares, absent from the metadata",
    BASE: "a base type the metadata names, whose class the model does not derive from",
    BETA: "a preview member the model does not mark",
    READONLY: "a service-assigned member the model sends",
    IGNORED: "a member the configured filters skip (not a gap)",
}

#: The prefix a class assumes when it states no type name of its own. SharePoint entity
#: classes answer ``"SP." + type(self).__name__`` (``sharepoint/entity.py``), so a class
#: that does not spell its name out has already named it; Graph classes each assign one.
DEFAULT_PREFIX = {"sharepoint": "SP"}

#: How many findings of a kind are listed before the report says how many it hid.
_SHOWN = 10

_FIELD = "field"
_CLASSVAR = "ClassVar"


@dataclass(frozen=True)
class Finding:
    """One member, and the way the model and the metadata disagree about it."""

    kind: str
    model: str
    type_name: str
    member: str
    detail: str = ""
    #: Where the model lives, so a report can be worked through file by file.
    path: str = ""

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "model": self.model,
            "type": self.type_name,
            "member": self.member,
            "detail": self.detail,
            "path": self.path,
        }


@dataclass(frozen=True)
class Declared:
    """One member as the source spells it."""

    name: str
    #: ``True``/``False`` for the roots a ``beta=`` keyword names, a string for a preview
    #: spelling, ``None`` when the declaration says nothing.
    beta: object = None
    readonly: bool = False
    #: ``False`` for a dataclass field with no ``odata(...)`` metadata: the attribute
    #: exists and serializes under its own name, and the schema knows nothing about it.
    declared: bool = True


@dataclass
class DeclaredModel:
    """One class, the OData type it says it describes, and its members."""

    path: Path
    name: str
    type_name: str
    members: Dict[str, Declared] = field(default_factory=dict)
    #: The classes the model derives from -- the file each is imported from, or ``None``
    #: when the module declares it itself -- so a member it inherits is still a member it
    #: serves: ``SP.Web`` answers a select with its base's columns.
    bases: Tuple[Tuple[Optional[Path], str], ...] = ()
    #: The models the class derives from, nearest first, filled in by :func:`_inherit`.
    ancestors: Tuple["DeclaredModel", ...] = ()


@dataclass(frozen=True)
class _Fact:
    """One member as the metadata spells it."""

    type_name: str = ""
    beta: bool = False
    readonly: bool = False


def read_models(root: Path, prefix: str = "", generated: Optional[Path] = None) -> List[DeclaredModel]:
    """Every class under ``root``, the OData type it states, and the module it bases on.

    A class that states no type name is read too, with an empty one: ``Entity`` computes
    its name at runtime, and every Graph model answers ``id`` from it. Skipping it would
    make the whole of ``id`` a column the model does not serve.

    ``prefix`` stands in for the name such a class computes at runtime, and applies only
    under ``generated`` (default: ``root``) -- the packages the generator writes. A
    hand-written class called ``User`` is not ``SP.User`` and is not judged as one.
    """
    named_under = generated if generated is not None else root
    models: List[DeclaredModel] = []
    for path in sorted(root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        imported = _imports(tree, root)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            models.append(
                DeclaredModel(
                    path=path,
                    name=node.name,
                    type_name=_odata_type_name(node) or (_prefix(prefix, node.name, path, named_under)),
                    members={declared.name: declared for declared in _members(node)},
                    bases=tuple((imported.get(_call_name(base)), _call_name(base)) for base in node.bases),
                )
            )
    _inherit(models)
    return models


def _prefix(prefix: str, name: str, path: Path, generated: Path) -> str:
    """The name a class computes at runtime, when the class is one the generator wrote."""
    return f"{prefix}.{name}" if prefix and generated in path.parents else ""


def _imports(tree: ast.Module, root: Path) -> Dict[str, Path]:
    """Local class name -> the file this module imports it from.

    By name alone two packages' ``Base`` classes are one class, and a member folded from
    the wrong one is a finding about a model that never inherited it.
    """
    found: Dict[str, Path] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or node.level or not node.module:
            continue
        target = _module_file(root, node.module)
        if target is not None:
            for alias in node.names:
                found[alias.asname or alias.name] = target
    return found


def _module_file(root: Path, module: str) -> Optional[Path]:
    """``office365.sharepoint.webs.web`` -> the file declaring it, when the walk read one."""
    parts = module.split(".")
    for base in (root, *root.parents):
        if base.name != parts[0]:
            continue
        directory = base.parent.joinpath(*parts)
        for candidate in (directory.with_suffix(".py"), directory / "__init__.py"):
            if candidate.is_file():
                return candidate
    return None


def _inherit(models: Sequence[DeclaredModel]) -> None:
    """Fold each model's ancestors' members into it, nearest declaration winning."""
    by_path = {(model.path, model.name): model for model in models}
    by_name: Dict[str, List[DeclaredModel]] = {}
    for model in models:
        by_name.setdefault(model.name, []).append(model)
    resolved: Dict[int, Tuple[Dict[str, Declared], Tuple[DeclaredModel, ...]]] = {}

    def _base_of(module: Optional[Path], name: str) -> Optional[DeclaredModel]:
        if module is not None:
            return by_path.get((module, name))
        candidates = by_name.get(name, []) if name else []
        return candidates[0] if len(candidates) == 1 else None

    def _resolve(model: DeclaredModel, seen: frozenset) -> Tuple[Dict[str, Declared], Tuple[DeclaredModel, ...]]:
        if id(model) in resolved:
            return resolved[id(model)]
        members: Dict[str, Declared] = {}
        ancestors: Dict[int, DeclaredModel] = {}
        for module, name in model.bases:
            base = _base_of(module, name)
            if base is None or id(base) in seen:
                continue
            base_members, base_ancestors = _resolve(base, seen | {id(base)})
            members.update(base_members)
            for ancestor in (*base_ancestors, base):
                ancestors.setdefault(id(ancestor), ancestor)
        members.update(model.members)
        resolved[id(model)] = (members, tuple(ancestors.values()))
        return resolved[id(model)]

    for model in models:
        model.members, model.ancestors = _resolve(model, frozenset({id(model)}))


def audit(
    models: Iterable[DeclaredModel],
    csdl: ODataModel,
    *,
    ignored_types: Sequence[str] = (),
    ignored_properties: Sequence[str] = (),
) -> List[Finding]:
    """The members ``models`` and ``csdl`` disagree about, in model order."""
    exact_ignored, prefix_ignored = split_ignored(list(ignored_types))
    ignored_props = frozenset(ignored_properties)
    declared_facts = declared_members(csdl)
    holders = _by_type(models)
    findings: List[Finding] = []
    for model in models:
        facts = declared_facts.get(model.type_name)
        if facts is None:
            continue
        base = _uninherited_base(model, csdl, holders)
        if base is not None:
            findings.append(base)
        for name, fact in facts.items():
            if name in ignored_props:
                findings.append(_ignored(model, name, "ignored_properties"))
            elif _is_ignored_type(fact.type_name, exact_ignored, prefix_ignored):
                findings.append(_ignored(model, name, fact.type_name))
            else:
                findings.extend(_disagreements(model, name, fact))
        findings.extend(_extras(model, facts))
    return findings


def _by_type(models: Iterable[DeclaredModel]) -> Dict[str, List[DeclaredModel]]:
    """The models that declare each OData type, so a metadata base can be named."""
    holders: Dict[str, List[DeclaredModel]] = {}
    for model in models:
        if model.type_name:
            holders.setdefault(model.type_name, []).append(model)
    return holders


def _uninherited_base(
    model: DeclaredModel, csdl: ODataModel, holders: Mapping[str, List[DeclaredModel]]
) -> Optional[Finding]:
    """The class the metadata's base names and this class does not derive from.

    A generated subclass keeps its base line -- it is source the generator preserves --
    so a base that was unrouted when the file was first written stays ``Entity``, and
    every column the base declares is a column the subclass answers nothing to.
    """
    schema = csdl.types.get(model.type_name)
    base_name = schema.BaseTypeName if schema is not None else None
    if not base_name:
        return None
    candidates = holders.get(base_name) or ()
    # Two models claiming one type is a disagreement of its own, and neither is the base.
    if len(candidates) != 1:
        return None
    expected = candidates[0]
    if any(ancestor is expected for ancestor in model.ancestors):
        return None
    return Finding(BASE, model.name, model.type_name, expected.name, base_name, str(model.path))


def declared_members(csdl: ODataModel) -> Dict[str, Dict[str, _Fact]]:
    """For each type, every member it serves -- its ancestors' included -- and its markers."""
    ancestors = csdl._ancestors()
    result: Dict[str, Dict[str, _Fact]] = {}
    for type_name, schema in csdl.types.items():
        facts: Dict[str, _Fact] = {}
        # Farthest ancestor first, so a type's own declaration is the one that stands.
        for source in (*reversed(ancestors[type_name]), schema):
            for name, prop in source.Properties.items():
                facts[name] = _Fact(
                    type_name=prop.TypeName or "",
                    beta=bool(prop.IsBeta),
                    readonly=bool(prop.ReadOnly),
                )
        result[type_name] = facts
    return result


def gaps(findings: Iterable[Finding]) -> List[Finding]:
    """The findings a model is expected to have none of."""
    return [finding for finding in findings if finding.kind in GAPS]


def render(findings: Sequence[Finding], base: Path) -> str:
    """The report: how many of each kind, then where the first ones are."""
    counts = {kind: sum(1 for finding in findings if finding.kind == kind) for kind in KINDS}
    lines = [f"{kind:<11} {counts[kind]:>5}  {_WHAT[kind]}" for kind in KINDS]
    for kind in KINDS:
        shown = [finding for finding in findings if finding.kind == kind][:_SHOWN]
        if not shown:
            continue
        lines.append("")
        lines.append(f"{kind}:")
        for finding in shown:
            suffix = f" -> {finding.detail}" if finding.detail else ""
            lines.append(f"  {_display(finding, base)}{suffix}")
        hidden = counts[kind] - len(shown)
        if hidden:
            lines.append(f"  ... and {hidden} more")
    return "\n".join(lines)


def write_report(findings: Sequence[Finding], path: str) -> None:
    """The findings as JSON, for a caller that wants to work through them."""
    Path(path).write_text(json.dumps([finding.to_dict() for finding in findings], indent=2), encoding="utf-8")


def _disagreements(model: DeclaredModel, name: str, fact: _Fact) -> Iterator[Finding]:
    def _finding(kind: str, detail: str = "") -> Finding:
        return Finding(kind, model.name, model.type_name, name, detail, str(model.path))

    declared = model.members.get(name)
    if declared is None:
        yield _finding(MISSING, fact.type_name)
        return
    if not declared.declared:
        yield _finding(UNDECLARED, _FIELD)
    if fact.beta and declared.beta is not True:
        yield _finding(BETA)
    if fact.readonly and not declared.readonly:
        yield _finding(READONLY)


def _ignored(model: DeclaredModel, name: str, detail: str) -> Finding:
    return Finding(IGNORED, model.name, model.type_name, name, detail, str(model.path))


def _extras(model: DeclaredModel, facts: Mapping[str, _Fact]) -> Iterator[Finding]:
    for name in model.members:
        if name not in facts:
            yield Finding(EXTRA, model.name, model.type_name, name, path=str(model.path))


def _display(finding: Finding, base: Path) -> str:
    location = finding.path
    try:
        location = str(Path(finding.path).relative_to(base))
    except ValueError:
        pass
    return f"{location}: {finding.type_name}.{finding.member}"


def _is_ignored_type(type_name: str, exact: Sequence[str], prefix: Sequence[str]) -> bool:
    """Whether the member's own type is one the generator does not model.

    A column typed as an ignored type cannot be declared by anything: the property's
    value has no class to hold it, which is why the generator drops the property with
    the type. ``ShieldAddRoleAssignmentPushdown`` is not this case -- it is an
    ``ignored_properties`` entry -- and neither is a member whose type resolves.
    """
    if not type_name:
        return False
    name = _unwrapped(type_name)
    return name in exact or any(name.startswith(prefix) for prefix in prefix)


def _unwrapped(type_name: str) -> str:
    """``Collection(SP.Alert)`` -> ``SP.Alert``; anything else as given."""
    if type_name.startswith("Collection(") and type_name.endswith(")"):
        return type_name[len("Collection(") : -1]
    return type_name


def _odata_type_name(node: ast.ClassDef) -> Optional[str]:
    """The OData type name a class states, in either spelling the tree uses.

    Graph assigns ``_odata_type_name``; SharePoint answers it from a property, because
    its names are not one namespace and the value is part of the class's own story.
    """
    for statement in node.body:
        if isinstance(statement, ast.Assign):
            targets = [target.id for target in statement.targets if isinstance(target, ast.Name)]
            if targets == ["_odata_type_name"]:
                return _string(statement.value)
        elif isinstance(statement, ast.FunctionDef) and statement.name == "entity_type_name":
            for line in ast.walk(statement):
                if isinstance(line, ast.Return):
                    return _string(line.value)
    return None


def _string(node: Optional[ast.expr]) -> Optional[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _members(node: ast.ClassDef) -> Iterator[Declared]:
    """The members a class body states: an ``@odata`` getter, or an annotated field."""
    for statement in node.body:
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            keywords = _odata_keywords(statement.decorator_list)
            if keywords is not None:
                yield _declared(keywords, statement.name)
        elif isinstance(statement, ast.AnnAssign):
            declared = _field(statement)
            if declared is not None:
                yield declared


def _declared(keywords: Mapping[str, ast.expr], attr: str) -> Declared:
    name = _string(keywords.get("name")) or _string(keywords.get("__positional__")) or attr
    beta = keywords.get("beta")
    return Declared(
        name=name,
        beta=beta.value if isinstance(beta, ast.Constant) else None,
        readonly=_is_true(keywords.get("readonly")),
        declared=True,
    )


def _field(statement: ast.AnnAssign) -> Optional[Declared]:
    """A dataclass field: a declaration when it carries ``odata(...)``, a bare field otherwise."""
    target = statement.target
    if not isinstance(target, ast.Name) or target.id.startswith("_") or _is_classvar(statement.annotation):
        return None
    if statement.value is None:
        return None  # a bare annotation states no field, which is what a dataclass sees too
    keywords = _field_keywords(statement.value)
    if keywords is None:
        return Declared(name=target.id, declared=False)
    return _declared(keywords, target.id)


def _is_classvar(annotation: Optional[ast.expr]) -> bool:
    text = ast.unparse(annotation) if annotation is not None else ""
    return text.startswith(_CLASSVAR)


def _field_keywords(node: Optional[ast.expr]) -> Optional[Mapping[str, ast.expr]]:
    """The ``odata(...)`` keywords of ``field(metadata=odata(...))``, when there are any."""
    if not isinstance(node, ast.Call) or _call_name(node.func) != _FIELD:
        return None
    for keyword in node.keywords:
        if keyword.arg == "metadata":
            return _odata_keywords([keyword.value])
    return None


def _odata_keywords(decorators: Sequence[ast.expr]) -> Optional[Mapping[str, ast.expr]]:
    """The keywords of the ``odata(...)`` call among ``decorators``, if one is there."""
    for decorator in decorators:
        if isinstance(decorator, ast.Call) and _call_name(decorator.func) == "odata":
            keywords: Dict[str, ast.expr] = {keyword.arg: keyword.value for keyword in decorator.keywords if keyword.arg}
            if decorator.args:
                # ``odata("emailAddress", ...)`` spells the name positionally.
                keywords["__positional__"] = decorator.args[0]
            return keywords
    return None


def _call_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _is_true(node: Optional[ast.expr]) -> bool:
    return isinstance(node, ast.Constant) and node.value is True
