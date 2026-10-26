"""Offline tests for the typed, immutable BuilderContext."""

from __future__ import annotations

from generator.builders.context import BuilderContext


def test_methods_enabled_variants() -> None:
    assert BuilderContext("/o", generate_methods="YES").methods_enabled
    assert not BuilderContext("/o", generate_methods="false").methods_enabled
    assert not BuilderContext("/o").methods_enabled


def test_with_plan_returns_an_enriched_copy() -> None:
    context = BuilderContext(output_path="/o")

    planned = context.with_plan(
        known_types=frozenset({"SP.Foo"}),
        type_modules={"SP.Foo": "office365.foo"},
        cyclic_types=frozenset(),
        enum_defaults={},
        inherited_members={},
    )

    assert planned.known_types == frozenset({"SP.Foo"})
    assert context.known_types == frozenset()  # original untouched
