"""The generation plan: everything a pass derives from the model before building a type.

Planning is a pure function of the model, the options and the type filter, so it lives
here rather than in the pipeline constructor and can be tested on a small model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Tuple

from generator.build.context import BuilderContext
from generator.build.intrinsic_members import intrinsic_members
from generator.build.member import sanitize_member_name
from generator.build.naming import normalize_member_key
from generator.core.config import GeneratorOptions
from generator.model_index.resolution import TypeRegistry
from generator.odata.model import ODataModel
from generator.odata.property import PropertyInformation
from generator.planning.cycles import find_cyclic_types
from generator.planning.filters import TypeFilter
from generator.planning.routing import Router, planned_module


def _pollable_types(model: ODataModel) -> frozenset[str]:
    """Entity types that model a long-running/async operation.

    A type is pollable when it or any ancestor in the CSDL base chain is an
    ``*Operation`` entity with a ``status`` property (``LongRunningOperation``,
    ``security.CaseOperation``, ``PrintOperation`` …); subtypes inherit it. Such
    types get the ``PollableOperation`` mixin so ``wait()`` / ``wait_async()``
    work on them.
    """

    def is_operation_with_status(name: str) -> bool:
        schema = model.types.get(name)
        return (
            bool(schema)
            and name.rsplit(".", 1)[-1].endswith("Operation")
            and any(prop.lower() == "status" for prop in schema.Properties)
        )

    def walk(name: str) -> bool:
        seen: set[str] = set()
        while name and name not in seen:
            seen.add(name)
            if is_operation_with_status(name):
                return True
            schema = model.types.get(name)
            name = (getattr(schema, "BaseTypeName", None) or "") if schema else ""
        return False

    return frozenset(
        name for name, schema in model.types.items() if schema.BaseTypeFullName == "EntityType" and walk(name)
    )


def _qualified_types(requested: Iterable[str], model: ODataModel) -> Tuple[Tuple[str, ...], Dict[str, str]]:
    """The model's own spelling of each requested type, and why the rest cannot be used.

    ``--type Event`` and ``--type microsoft.graph.Event`` mean the same thing, and both
    surfaces stayed reachable for a while: the pipeline wanted the qualified name while
    the marker plan accepted the short one, so the same flag worked in one mode and
    silently selected nothing in the other. The metadata decides here, as it does
    everywhere else -- and a short name two types share is reported, never guessed.
    """
    by_short: Dict[str, List[str]] = {}
    for name in model.types:
        by_short.setdefault(name.rsplit(".", maxsplit=1)[-1].lower(), []).append(name)
    qualified: List[str] = []
    unresolved: Dict[str, str] = {}
    for name in requested:
        if name in model.types:
            qualified.append(name)
            continue
        candidates = by_short.get(name.rsplit(".", maxsplit=1)[-1].lower(), [])
        if len(candidates) == 1:
            qualified.append(candidates[0])
        elif candidates:
            unresolved[name] = f"ambiguous, the metadata has {', '.join(sorted(candidates))}"
        else:
            unresolved[name] = "not in metadata"
    return tuple(qualified), unresolved


@dataclass(frozen=True)
class GenerationPlan:
    """What one pass will generate, and the cross-type facts builders rely on."""

    #: Types this run will generate (attached or routed); only these are importable by name.
    known_types: frozenset[str]
    type_modules: Mapping[str, str]
    #: First member per in-scope enum, so enum-typed fields default to it.
    enum_defaults: Mapping[str, str]
    cyclic_types: frozenset[str]
    inherited_members: Mapping[str, frozenset[str]]
    entity_types: frozenset[str]
    client_value_types: frozenset[str]
    pollable_types: frozenset[str]
    declared_properties: Mapping[str, frozenset[str]]
    intrinsic_properties: Mapping[str, Tuple[PropertyInformation, ...]]

    def apply(self, context: BuilderContext) -> BuilderContext:
        """The builder context enriched with this plan."""
        return context.with_plan(
            known_types=self.known_types,
            type_modules=self.type_modules,
            cyclic_types=self.cyclic_types,
            enum_defaults=self.enum_defaults,
            inherited_members=self.inherited_members,
            entity_types=self.entity_types,
            client_value_types=self.client_value_types,
            pollable_types=self.pollable_types,
            declared_properties=self.declared_properties,
            intrinsic_properties=self.intrinsic_properties,
        )


class PlanBuilder:
    """Derives a :class:`GenerationPlan` from a model."""

    @staticmethod
    def build(
        model: ODataModel,
        options: GeneratorOptions,
        type_filter: TypeFilter,
        context: BuilderContext,
        only_types: frozenset[str] = frozenset(),
    ) -> GenerationPlan:
        """The plan for one pass.

        ``only_types`` is what a ``--type``-filtered run will actually write. Without it
        the plan describes the whole metadata, so ``known_types`` -- documented above as
        "types this run will generate" -- claimed every routed type, and a builder asking
        whether a reference was importable answered yes for a file nobody was writing.
        A whole-metadata pass leaves it empty and is unaffected.
        """
        router = Router.from_options(context)
        registry = TypeRegistry(options.modules.split(","), namespace=options.namespace)
        known_types: set[str] = set()
        type_modules: dict[str, str] = {}
        for name, schema in model.types.items():
            if only_types and name not in only_types:
                continue
            if not type_filter.in_scope(name, schema):
                continue
            module = planned_module(name, schema, registry, router, options.output_path)
            if module is not None:
                known_types.add(name)
                type_modules[name] = module
        enum_defaults: dict[str, str] = {}
        for name, schema in model.types.items():
            if schema.BaseTypeFullName == "EnumType" and type_filter.in_scope(name, schema):
                enum_defaults[name] = next((sanitize_member_name(m) for m in schema.Members), "")
        return GenerationPlan(
            known_types=frozenset(known_types),
            type_modules=type_modules,
            enum_defaults=enum_defaults,
            cyclic_types=frozenset(find_cyclic_types(model, known_types)),
            inherited_members=model.inherited_member_names(),
            entity_types=frozenset(
                name for name, schema in model.types.items() if schema.BaseTypeFullName == "EntityType"
            ),
            client_value_types=frozenset(
                name for name in known_types if model.types[name].BaseTypeFullName != "EntityType"
            ),
            pollable_types=_pollable_types(model),
            declared_properties={
                name: frozenset(normalize_member_key(key) for key in keys)
                for name, keys in model.effective_property_names().items()
            },
            intrinsic_properties=intrinsic_members(model),
        )
