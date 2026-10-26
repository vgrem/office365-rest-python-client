"""Typed, immutable configuration passed to the builders.

One type, not a free-form ``dict`` (string keys, no validation): a builder either
receives a context or an empty one, and every knob has a name the checker sees.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Mapping


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
    #: In-scope types whose CSDL base chain is a long-running/async operation
    #: (they get the ``PollableOperation`` mixin so they can be awaited).
    pollable_types: frozenset[str] = frozenset()
    inherited_members: Mapping[str, frozenset[str]] = field(default_factory=dict)
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
        pollable_types: frozenset[str] = frozenset(),
    ) -> "BuilderContext":
        """Return a copy enriched with the run plan (known types, modules, cycles)."""
        return replace(
            self,
            known_types=known_types,
            type_modules=dict(type_modules),
            cyclic_types=cyclic_types,
            enum_defaults=dict(enum_defaults),
            entity_types=frozenset(entity_types),
            pollable_types=frozenset(pollable_types),
            inherited_members={name: frozenset(members) for name, members in inherited_members.items()},
        )
