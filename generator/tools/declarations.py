"""Declaration rules checked over the rendered model."""

from __future__ import annotations

import ast
import importlib
import pkgutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional, Sequence, Set, Tuple, Type, get_origin, get_type_hints

if TYPE_CHECKING:
    from types import ModuleType

_NOT_A_PACKAGE = frozenset({"__pycache__"})
_SHAREPOINT = "sharepoint"

SERVED = "packages served"
WITNESS = "a declaration names a name its getter reads"
TYPED = "every projected column declares a type"
NAVIGATION = "a client object member is a navigation"
FACET = "a facet keyword names one of the declared roles"

RULES = (SERVED, WITNESS, TYPED, NAVIGATION, FACET)

#: A rule whose subjects stop resolving reports "ok" while checking nothing.
MIN_SERVED = 20
MIN_PROJECTED = 11_000
MIN_NAVIGATIONS = 800
MIN_FACETED = 4

_SHOWN = 20

_UNITS = {SERVED: "packages", WITNESS: "members", TYPED: "columns", NAVIGATION: "members", FACET: "members"}


@dataclass
class DeclarationReport:
    package: Path
    roots: Tuple[Path, ...]
    findings: Dict[str, List[str]] = field(default_factory=dict)
    checked: Dict[str, int] = field(default_factory=dict)

    def record(self, rule: str, findings: Sequence[str], checked: int) -> None:
        self.findings[rule] = list(findings)
        self.checked[rule] = checked

    @property
    def ok(self) -> bool:
        return not any(self.findings.get(rule) for rule in RULES)

    def to_dict(self) -> dict:
        return {
            "package": str(self.package),
            "count_packages": len(self.roots),
            "ok": self.ok,
            "rules": {
                rule: {"checked": self.checked.get(rule, 0), "findings": self.findings.get(rule, [])} for rule in RULES
            },
        }

    def render(self) -> str:
        lines = [f"model declarations: {self.package} ({len(self.roots)} packages)"]
        for rule in RULES:
            count, found = self.checked.get(rule, 0), self.findings.get(rule, [])
            status = f", {len(found)} findings" if found else ""
            lines.append(f"  {'FAIL' if found else 'ok  '} {rule} ({count:,} {_UNITS[rule]}{status})")
            lines.extend(f"         {detail}" for detail in found[:_SHOWN])
            if len(found) > _SHOWN:
                lines.append(f"         ... and {len(found) - _SHOWN:,} more")
        return "\n".join(lines)


def model_package() -> Path:
    return Path(__file__).resolve().parents[2] / "office365"


def model_roots(package: Path) -> List[Path]:
    """Every package the model is generated for, derived from the tree."""
    packages = sorted(entry for entry in package.iterdir() if entry.is_dir() and entry.name not in _NOT_A_PACKAGE)
    return [entry for entry in packages if entry.name != _SHAREPOINT] + [
        entry for entry in packages if entry.name == _SHAREPOINT
    ]


def served_packages(package: Path) -> Tuple[List[str], int]:
    roots = model_roots(package)
    served = {root.name for root in roots}
    uncovered = [
        entry.name
        for entry in sorted(package.iterdir())
        if entry.is_dir() and entry.name not in served and entry.name not in _NOT_A_PACKAGE
    ]
    return uncovered, len(roots)


def witness_disagreements(package: Path) -> Tuple[List[str], int]:
    """A declaration must name a wire name its getter body reads."""
    findings: List[str] = []
    checked = 0
    for path in _sources(model_roots(package)):
        for cls in _classes(path.read_text(encoding="utf-8")):
            for getter in _getters(cls):
                declared, spelled = _declared_name(getter), _spelled_names(getter)
                if declared is None or not spelled:
                    continue
                checked += 1
                if declared not in spelled:
                    findings.append(
                        f"{path.relative_to(package)} {cls.name}.{getter.name} declares {declared!r},"
                        f" reads {sorted(spelled)}"
                    )
    return findings, checked


def untyped_columns(package: Path) -> Tuple[List[str], int]:
    """Every projected column must resolve to the type its getter returns."""
    from office365.runtime.client_object import ClientObject
    from office365.runtime.converters.value import declared_type
    from office365.runtime.schema import TypeSchema

    findings: List[str] = []
    checked = 0
    for module in _modules(package):
        for cls in _declared_types(module, ClientObject):
            for name in TypeSchema.of(cls).columns:
                checked += 1
                if declared_type(cls, name) is None:
                    findings.append(f"{cls.__module__}.{cls.__name__}.{name}")
    return findings, checked


def navigation_disagreements(package: Path) -> Tuple[List[str], int]:
    """A getter that returns a client object names a member reached by ``$expand``.

    The other direction does not hold: SharePoint v3 hydrates a navigation as a value
    (``SitePage.created_by`` is a ``UserInfo``), so a value-typed getter on a declared
    navigation is a fact about that service, not a disagreement.
    """
    from office365.runtime.client_object import ClientObject
    from office365.runtime.client_object_collection import ClientObjectCollection

    findings: List[str] = []
    checked = 0
    for module in _modules(package):
        for cls in _declared_types(module, ClientObject):
            for attr, name in cls._schema.by_attr.items():
                kind = _annotation_kind(cls, attr, ClientObject, ClientObjectCollection)
                if kind is None:
                    continue
                if kind != "object":
                    continue
                checked += 1
                declared = cls._schema.properties[name]
                if not declared.navigation:
                    findings.append(f"{cls.__module__}.{cls.__name__}.{attr}: a client object declared as a column")
    return findings, checked


def facet_disagreements(package: Path) -> Tuple[List[str], int]:
    """A ``facet=`` keyword is spelled with one of the role constants, not a string."""
    roles = _facet_roles()
    findings: List[str] = []
    checked = 0
    for path in _sources(model_roots(package)):
        for cls in _classes(path.read_text(encoding="utf-8")):
            for getter in _getters(cls):
                for spelling in _facet_spellings(getter):
                    checked += 1
                    if spelling not in roles:
                        findings.append(f"{path.relative_to(package)} {cls.name}.{getter.name} facet={spelling}")
    return findings, checked


def declaration_report(package: Optional[Path] = None) -> DeclarationReport:
    package = Path(package) if package is not None else model_package()
    report = DeclarationReport(package=package, roots=tuple(model_roots(package)))
    floors = {SERVED: MIN_SERVED, TYPED: MIN_PROJECTED, NAVIGATION: MIN_NAVIGATIONS, FACET: MIN_FACETED}
    for rule, run in (
        (SERVED, served_packages),
        (WITNESS, witness_disagreements),
        (TYPED, untyped_columns),
        (NAVIGATION, navigation_disagreements),
        (FACET, facet_disagreements),
    ):
        findings, checked = run(package)
        floor = floors.get(rule)
        if floor is not None and checked < floor:
            findings = [*findings, f"checked {checked:,} of a floor of {floor:,}"]
        report.record(rule, findings, checked)
    return report


def _sources(roots: Sequence[Path]) -> Iterator[Path]:
    for root in roots:
        yield from sorted(root.rglob("*.py"))


def _classes(text: str) -> Iterator[ast.ClassDef]:
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.ClassDef):
            yield node


def _getters(cls: ast.ClassDef) -> Iterator[ast.FunctionDef]:
    """The class's own property getters; a method's declaration names a function import."""
    for node in cls.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        markers = [marker for marker in node.decorator_list if not isinstance(marker, ast.Call)]
        if any(getattr(marker, "id", "") == "property" for marker in markers):
            yield node


def _facet_roles() -> Dict[str, str]:
    """The names a facet may be spelled with, and the role each one declares."""
    from office365.runtime.types import odata_property

    roles = odata_property.FACETS
    return {name: value for name, value in vars(odata_property).items() if isinstance(value, str) and value in roles}


def _facet_spellings(getter: ast.FunctionDef) -> Iterator[str]:
    """The ``facet=`` values of a getter's ``@odata`` call, spelled as the source spells them."""
    for decorator in getter.decorator_list:
        if not isinstance(decorator, ast.Call) or getattr(decorator.func, "id", "") != "odata":
            continue
        for keyword in decorator.keywords:
            value = keyword.value
            if keyword.arg != "facet":
                continue
            if isinstance(value, ast.Name):
                yield value.id
            elif isinstance(value, ast.Constant) and isinstance(value.value, str):
                yield value.value


def _declared_name(getter: ast.FunctionDef) -> Optional[str]:
    for decorator in getter.decorator_list:
        if isinstance(decorator, ast.Call) and getattr(decorator.func, "id", "") == "odata":
            for keyword in decorator.keywords:
                if keyword.arg == "name" and isinstance(keyword.value, ast.Constant):
                    return str(keyword.value.value)
    return None


def _spelled_names(getter: ast.FunctionDef) -> Set[str]:
    """Every wire name the body reads off ``self.properties``."""
    names: Set[str] = set()
    for node in ast.walk(getter):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get":
            owner = node.func.value
            literal = node.args[0] if node.args else None
            if isinstance(owner, ast.Attribute) and owner.attr == "properties" and isinstance(literal, ast.Constant):
                if isinstance(literal.value, str):
                    names.add(literal.value)
        elif (
            isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute) and node.value.attr == "properties"
        ):
            if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
                names.add(node.slice.value)
    return names


def _modules(package: Path) -> Iterator[ModuleType]:
    for info in pkgutil.walk_packages([str(package)], prefix=f"{package.name}."):
        yield importlib.import_module(info.name)


def _declared_types(module: ModuleType, base: Type) -> Iterator[type]:
    for member in vars(module).values():
        if isinstance(member, type) and issubclass(member, base) and member.__module__ == module.__name__:
            yield member


def _annotation_kind(cls: type, attr: str, *bases: Type) -> Optional[str]:
    """``"object"`` or ``"value"`` from a getter's annotation, ``None`` when unresolvable."""
    prop = getattr(cls, attr, None)
    if not isinstance(prop, property) or prop.fget is None:
        return None
    try:
        hint = get_type_hints(prop.fget).get("return")
    except Exception:  # noqa: BLE001 - a TYPE_CHECKING-only import cannot be resolved at runtime
        return None
    target = get_origin(hint) or hint
    if not isinstance(target, type):
        return None
    return "object" if issubclass(target, bases) else "value"
