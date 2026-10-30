"""Typed, immutable configuration passed to the builders.

One type, not a free-form ``dict`` (string keys, no validation): a builder either
receives a context or an empty one, and every knob has a name the checker sees.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Mapping, Tuple

from generator.odata.property import PropertyInformation

#: Shared empty mapping, so a defaulted ``Mapping`` parameter is not a mutable literal.
_NO_PROPERTIES: Mapping[str, frozenset[str]] = MappingProxyType({})
_NO_INTRINSIC: Mapping[str, Tuple[PropertyInformation, ...]] = MappingProxyType({})


@dataclass(frozen=True)
class BuilderContext:
    """Everything a :class:`~generator.builders.type.TypeBuilder` needs."""

    output_path: str = ""
    modules: str = ""
    namespace: str = ""
    context_type: str = "ClientContext"
    generate_methods: str = ""
    ignored_properties: tuple[str, ...] = ()
    ignored_methods: tuple[str, ...] = ()
    routing: Mapping[str, str] = field(default_factory=dict)
    type_routing: Mapping[str, str] = field(default_factory=dict)
    known_types: frozenset[str] = frozenset()
    type_modules: Mapping[str, str] = field(default_factory=dict)
    cyclic_types: frozenset[str] = frozenset()
    enum_defaults: Mapping[str, str] = field(default_factory=dict)
    entity_types: frozenset[str] = frozenset()
    #: Types this run will write that the CSDL declares as something other than an
    #: ``EntityType``. A type written by the run has no module to import yet, so an
    #: operation returning one cannot be classified by inspecting its class: the
    #: metadata already says what it is.
    client_value_types: frozenset[str] = frozenset()
    #: In-scope types whose CSDL base chain is a long-running/async operation
    #: (they get the ``PollableOperation`` mixin so they can be awaited).
    pollable_types: frozenset[str] = frozenset()
    inherited_members: Mapping[str, frozenset[str]] = field(default_factory=dict)
    #: Every type's property names with its ancestors' folded in, as normalized
    #: member keys. Asked when a class's ``entity_type_name`` names a type other
    #: than the one being built: its members say which type it actually models.
    declared_properties: Mapping[str, frozenset[str]] = field(default_factory=dict)
    #: Members every subtype of a type declares and the type itself does not, so the
    #: base type carries them by construction (see :mod:`generator.intrinsic_members`).
    intrinsic_properties: Mapping[str, Tuple[PropertyInformation, ...]] = field(default_factory=dict)
    dry_run: bool = False

    @property
    def methods_enabled(self) -> bool:
        """Whether operation method generation is enabled."""
        return str(self.generate_methods).strip().lower() in {"true", "1", "yes"}

    def with_plan(
        self,
        *,
        known_types: frozenset[str],
        type_modules: Mapping[str, str],
        cyclic_types: frozenset[str],
        enum_defaults: Mapping[str, str],
        inherited_members: Mapping[str, frozenset[str]],
        entity_types: frozenset[str] = frozenset(),
        client_value_types: frozenset[str] = frozenset(),
        pollable_types: frozenset[str] = frozenset(),
        declared_properties: Mapping[str, frozenset[str]] = _NO_PROPERTIES,
        intrinsic_properties: Mapping[str, Tuple[PropertyInformation, ...]] = _NO_INTRINSIC,
    ) -> "BuilderContext":
        """Return a copy enriched with the run plan (known types, modules, cycles)."""
        return replace(
            self,
            known_types=known_types,
            type_modules=dict(type_modules),
            cyclic_types=cyclic_types,
            enum_defaults=dict(enum_defaults),
            entity_types=frozenset(entity_types),
            client_value_types=frozenset(client_value_types),
            pollable_types=frozenset(pollable_types),
            inherited_members={name: frozenset(members) for name, members in inherited_members.items()},
            declared_properties={name: frozenset(names) for name, names in declared_properties.items()},
            intrinsic_properties=dict(intrinsic_properties),
        )
