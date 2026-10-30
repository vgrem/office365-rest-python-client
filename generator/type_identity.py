"""Which CSDL type a class actually models.

Two CSDL types resolve to one module when they share a short name: ``descend_module``
names the file after the class, so ``microsoft.graph.Alert`` and
``microsoft.graph.security.Alert`` both land in ``office365/security/alerts/alert.py``.
The file then defines one class, and ``entity_type_name`` answers with whichever type
the class was first written for -- which is not necessarily the one its members came
from. Answering with the wrong name tells every metadata reader that the service has
never heard of the members the class declares, which is exactly what ``system=True``
claims (``mark_odata.py``), so the name is decided here, from the class's own members.

The decision is deliberately one-sided: a *witness* member name the candidate declares
and the current name does not, and no member the other way round. A class that also
spells something only its own type declares is not misnamed -- it is answering for a
type the snapshot has not caught up with -- and is left alone.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Callable, Dict, Iterable, Mapping, NamedTuple, Optional, Tuple

from generator.builders.naming import normalize_member_key
from generator.builders.node_factory import declared_wire_name

#: ``self.properties.<name>(...)`` calls that read a column by its wire name.
_READERS = {"get", "setdefault"}


class Modelled(NamedTuple):
    """One class, the name it answers with, and what its members say about that."""

    module: str
    class_name: str
    declared: Optional[str]
    verdict: str
    detail: str = ""


def spelled_names(getter: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """The wire names a method spells: its ``@odata(name=...)`` and its column reads."""
    names = {declared_wire_name(getter)} - {""}
    for node in ast.walk(getter):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr not in _READERS or not node.args:
            continue
        owner = node.func.value
        if isinstance(owner, ast.Attribute) and owner.attr == "properties":
            first = node.args[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                names.add(first.value)
    return names


def class_spellings(class_node: ast.ClassDef) -> frozenset[str]:
    """Every wire name the class's methods spell, as normalized member keys."""
    names: set[str] = set()
    for stmt in class_node.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names |= spelled_names(stmt)
    return frozenset(normalize_member_key(name) for name in names)


def entity_type_name_return(class_node: ast.ClassDef) -> Optional[ast.Return]:
    """The ``return "<literal>"`` of the class's own ``entity_type_name``, when that is its shape.

    Only a single-line string return is answered: the name is rewritten a line at a
    time, so a getter that computes it is reported rather than edited.
    """
    for stmt in class_node.body:
        if not isinstance(stmt, ast.FunctionDef) or stmt.name != "entity_type_name":
            continue
        for node in ast.walk(stmt):
            if not isinstance(node, ast.Return) or not isinstance(node.value, ast.Constant):
                continue
            if isinstance(node.value.value, str) and node.end_lineno == node.lineno:
                return node
    return None


def entity_type_name_literal(class_node: ast.ClassDef) -> Optional[str]:
    """The literal a class's own ``entity_type_name`` returns, or ``None``."""
    node = entity_type_name_return(class_node)
    value = node.value if node is not None else None
    return value.value if isinstance(value, ast.Constant) and isinstance(value.value, str) else None


def identity_evidence(
    class_node: ast.ClassDef,
    *,
    declared: str,
    candidate: str,
    declared_properties: Mapping[str, frozenset[str]],
) -> Tuple[frozenset[str], frozenset[str]]:
    """The member names that argue for ``candidate`` and those that argue against it.

    ``declared`` is what the class answers with today, ``candidate`` the type being
    generated from the CSDL. A name the snapshot does not contain cannot argue
    against anything -- it declares nothing -- so such a class is decided on the same
    evidence as one that answers with a sibling.
    """
    if declared.lower() == candidate.lower():
        # One type, two spellings: the model key Pascal-cases the CSDL's last segment
        # (``Microsoft.SharePoint.Comments.comment`` reads as ``...Comments.Comment``),
        # while ``entity_type_name`` answers with the name the wire uses. Not a rename.
        return frozenset(), frozenset()
    spelled = class_spellings(class_node)
    better = declared_properties.get(candidate, frozenset())
    own = declared_properties.get(declared, frozenset())
    return frozenset(spelled & (better - own)), frozenset(spelled & (own - better))


def modelled_type(
    class_node: ast.ClassDef,
    *,
    declared: str,
    candidate: str,
    declared_properties: Mapping[str, frozenset[str]],
) -> Optional[str]:
    """``candidate`` when the class's members say they belong to it, else ``None``.

    One-sided only: a witness and nothing against. A class that spells members of
    both types is not misnamed but merged -- two CSDL types sharing one module whose
    file grew each type's members on top of the other's -- and which of the two names
    it answers with is then a placement question, not a renaming one.
    """
    witness, refute = identity_evidence(
        class_node, declared=declared, candidate=candidate, declared_properties=declared_properties
    )
    return candidate if witness and not refute else None


def claimed_modules(
    model,
    *,
    registry,
    router,
    output_path: str = "",
    in_scope: Optional[Callable[[str, object], bool]] = None,
) -> Dict[str, Tuple[str, ...]]:
    """The modules more than one type of ``model`` resolves to, and who claims them.

    Placement is the generator's own (``planned_module``), not a guess: the same call
    the run uses to decide where a type is written. A module claimed by two types is
    one file holding one class for two member sets, so it has to be reviewed and is
    therefore frozen in ``tests/tooling/test_generator_type_identity.py``.
    """
    from generator.routing import planned_module

    claimed: dict[str, list[str]] = {}
    for name, schema in model.types.items():
        if in_scope is not None and not in_scope(name, schema):
            continue
        module = planned_module(name, schema, registry, router, output_path)
        if module:
            claimed.setdefault(module, []).append(name)
    return {module: tuple(sorted(names)) for module, names in sorted(claimed.items()) if len(names) > 1}


def audit(
    claims: Mapping[str, Iterable[str]],
    class_names: Mapping[str, str],
    declared_properties: Mapping[str, frozenset[str]],
    *,
    root: str = ".",
) -> list[Modelled]:
    """Decide, per class, whether the name it answers with is the type it models."""
    rows: list[Modelled] = []
    for module, names in claims.items():
        source = _source_of(module, root)
        tree = ast.parse(source) if source else None
        seen: set[str] = set()
        for name in names:
            class_name = class_names.get(name, name.rsplit(".", 1)[-1])
            if class_name in seen:
                continue
            seen.add(class_name)
            node = _class_node(tree, class_name)
            if node is None:
                rows.append(Modelled(module, class_name, None, "missing", name))
                continue
            declared = entity_type_name_literal(node)
            answer = declared or name
            evidence = {
                candidate: identity_evidence(
                    node, declared=answer, candidate=candidate, declared_properties=declared_properties
                )
                for candidate in names
                if candidate != answer
            }
            misnamed = [candidate for candidate, (witness, refute) in evidence.items() if witness and not refute]
            merged = [candidate for candidate, (witness, refute) in evidence.items() if witness and refute]
            if misnamed:
                rows.append(Modelled(module, class_name, answer, "misnamed", misnamed[0]))
            elif merged:
                rows.append(Modelled(module, class_name, answer, "merged", merged[0]))
            elif declared is None or declared not in names:
                rows.append(Modelled(module, class_name, answer, "unnamed", ""))
            else:
                rows.append(Modelled(module, class_name, answer, "agrees", ""))
    return rows


def _source_of(module: str, root: str) -> Optional[str]:
    path = Path(root, *module.split(".")).with_suffix(".py")
    return path.read_text(encoding="utf-8") if path.is_file() else None


def _class_node(tree: Optional[ast.Module], class_name: str) -> Optional[ast.ClassDef]:
    if tree is None:
        return None
    return next((node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == class_name), None)
