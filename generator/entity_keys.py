"""Which ``@key(...)`` a snapshot justifies, and which types deliberately get none.

A key is not a diff. One snapshot states it, so the plan is a pure function of that
snapshot *and* of what the model's own source already says -- a class that writes
``property_ref_name`` has answered the question itself, and a derivation that overwrote it
would be the generator deciding, on its own, what a service addresses an entity by. The
code is the state, the same way :mod:`generator.beta_markers` reads it.

The plan is deliberately narrow. Of Graph's 1,239 v1.0 entity types, 13 state a key and
1,226 inherit ``entity``'s. Four of the 13 state ``id`` -- the fallback, so there is
nothing to say -- and the remaining nine are the types a request addresses by a property
the client does not know about today. Two further shapes are refused on principle rather
than by count: a composite key (no single path segment exists to write it with, and the
preview snapshot declares one) and a key no class spells.

SharePoint is where the same derivation must **not** be trusted. Its v3 metadata states a
key on 613 of 871 entity types, and states ones no client can address an entity by:
``Alert`` by ``AlertFrequency``, ``TypeInformation`` by ``BaseTypeFullName``,
``ApiMetadata`` by ``Id4a81de82eeb94d6080ea5bf63e27023a``. The seventeen hand-written
``property_ref_name`` overrides under ``office365/sharepoint`` are the reviewed answer,
and they are not a subset of it -- thirteen agree, three contradict it
(``HubSiteProperties`` is addressed by ``SiteId``, not the metadata's ``Description``),
one names a type the snapshot does not declare. So SharePoint plans and reports; it does
not write, and :attr:`~generator.services.ServiceDefinition.keys_authoritative` is what
refuses the write.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from generator.marker_apply import TypeFiles

#: The decorator a plan writes, and the name the pass reports it under.
KEY = "key"


@dataclass(frozen=True)
class KeyMarker:
    """One ``@key(...)`` a class needs, and the CSDL type it belongs to."""

    type_name: str
    key: str

    def to_dict(self) -> dict:
        return {"type": self.type_name, "key": self.key}


@dataclass
class KeyPlan:
    """Every key declaration the snapshot justifies, and everything it does not."""

    metadata: str
    markers: List[KeyMarker] = field(default_factory=list)
    defaults: List[str] = field(default_factory=list)
    skipped: List[Tuple[KeyMarker, str]] = field(default_factory=list)

    def restricted(self, types: Iterable[str]) -> "KeyPlan":
        """The part of the plan that lands on ``types`` (short or qualified names)."""
        wanted = {name.rsplit(".", 1)[-1].lower() for name in types}
        matches = lambda marker: marker.type_name.rsplit(".", 1)[-1].lower() in wanted  # noqa: E731
        return KeyPlan(
            metadata=self.metadata,
            markers=[marker for marker in self.markers if matches(marker)],
            defaults=[name for name in self.defaults if name.rsplit(".", 1)[-1].lower() in wanted],
            skipped=[(marker, reason) for marker, reason in self.skipped if matches(marker)],
        )

    @property
    def is_empty(self) -> bool:
        return not self.markers

    def to_dict(self) -> dict:
        return {
            "metadata": self.metadata,
            "count": len(self.markers),
            "markers": [marker.to_dict() for marker in self.markers],
            "count_defaults": len(self.defaults),
            "defaults": self.defaults,
            "count_skipped": len(self.skipped),
            "skipped": [dict(marker.to_dict(), reason=reason) for marker, reason in self.skipped],
        }

    def render(self) -> str:
        text = f"{self.metadata} keys: {len(self.markers)} to declare"
        if self.defaults:
            text += f", {len(self.defaults)} already the default"
        if self.skipped:
            text += f", {len(self.skipped)} skipped"
        return text


def plan_keys(
    model,
    files: TypeFiles,
    *,
    metadata: str,
    default: str = "id",
    only: Optional[Iterable[str]] = None,
) -> KeyPlan:
    """The ``@key(...)`` every entity type of ``model`` needs, and why the rest need none.

    ``default`` is the key a type inherits when the document states none -- the family
    base's spelling, which is what most types rely on. A derivation that lands on it is
    not a marker: the marker would restate the fallback.
    """
    plan = KeyPlan(metadata=metadata)
    for type_name, schema in sorted(model.types.items()):
        if not schema.IsValueObject or not schema.Key:
            continue
        marker = KeyMarker(type_name, schema.Key[0])
        if len(schema.Key) > 1:
            plan.skipped.append((marker, f"a key of {len(schema.Key)} properties has no single path segment"))
            continue
        if marker.key == default:
            plan.defaults.append(type_name)
            continue
        refusal = _refusal(files, type_name, marker.key)
        if refusal is not None:
            plan.skipped.append((marker, refusal))
            continue
        plan.markers.append(marker)
    narrowed = list(only) if only is not None else []
    return plan.restricted(narrowed) if narrowed else plan


def _refusal(files: TypeFiles, type_name: str, key: str) -> Optional[str]:
    """Why ``type_name`` must not be decorated, or ``None`` when it may be."""
    located = files.class_for(type_name)
    if located is None:
        return "no class declares this type"
    _, class_node = located
    if not files.is_addressed(type_name):
        return "a complex or enum type is not addressed by a request"
    if _states_key_itself(files, type_name):
        return f"{class_node.name} states its key in property_ref_name"
    if not _holds(files, type_name, key):
        return f"no member of {class_node.name} is spelled {key}"
    return None


def _states_key_itself(files: TypeFiles, type_name: str) -> bool:
    """Whether a class in the chain answers ``property_ref_name`` with a literal.

    ``Entity`` and ``SP.Entity`` answer with an expression that *reads* the declaration,
    which is the fallback rather than a statement; a hand-written override answers with
    the string itself, and that is the fact the decorator would be duplicating.
    """
    for _, class_node in files.class_chain(type_name):
        for node in class_node.body:
            if not isinstance(node, ast.FunctionDef) or node.name != "property_ref_name":
                continue
            for statement in ast.walk(node):
                if isinstance(statement, ast.Return) and isinstance(statement.value, ast.Constant):
                    if isinstance(statement.value.value, str):
                        return True
    return False


def _holds(files: TypeFiles, type_name: str, key: str) -> bool:
    """Whether the class (or a base) carries ``key`` -- declared, or read by its wire name.

    Both shapes count because the tree is only half-declared: 48% of its members state an
    ``@odata(name=...)`` and the rest are still ``self.properties.get("tenantId", None)``.
    A key naming neither is a key for a member this class does not have, so the marker
    would be a decorator that can never take effect.
    """
    for _, class_node in files.class_chain(type_name):
        for node in ast.walk(class_node):
            if isinstance(node, ast.Call):
                if getattr(node.func, "id", None) == "odata" and _declares_name(node.keywords, key):
                    return True
                if isinstance(node.func, ast.Attribute) and node.func.attr == "get":
                    if node.args and _literal(node.args[0]) == key:
                        return True
            elif isinstance(node, ast.Subscript) and _literal(node.slice) == key:
                return True
    return False


def _declares_name(keywords: List[ast.keyword], key: str) -> bool:
    return any(keyword.arg == "name" and _literal(keyword.value) == key for keyword in keywords)


def _literal(node: ast.expr) -> Optional[str]:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def write_report(plan: KeyPlan, path: str) -> None:
    """Write the plan itself, so a reviewer can diff what the pass would change."""
    import json

    Path(path).write_text(json.dumps(plan.to_dict(), indent=2) + "\n", encoding="utf-8")
