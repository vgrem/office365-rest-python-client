"""Offline tests for YAML config loading, validation, and the typed context it builds."""

from __future__ import annotations

from pathlib import Path

import pytest
from generator.builders.context import BuilderContext
from generator.config import ConfigError, GeneratorOptions, parse_list, split_ignored

_BASE = """
metadata_path: ./metadata/Graph.xml
output_path: ./office365
modules: [office365]
"""


def _write(tmp_path: Path, body: str) -> None:
    (tmp_path / "office365").mkdir(exist_ok=True)
    (tmp_path / "settings.graph.yaml").write_text(body, encoding="utf-8")


def test_load_reads_typed_options(tmp_path: Path) -> None:
    _write(
        tmp_path,
        _BASE
        + """
context_type: GraphClient
generate_methods: true
include_base_types: [ComplexType, EnumType]
filters:
  ignored_types: [microsoft.graph.X, "microsoft.graph.Edu*"]
routing:
  microsoft.graph.foo: office365.foo
type_routing:
  "Bar*": office365.bar
""",
    )

    options = GeneratorOptions.load("graph", tmp_path)

    assert options.include_base_types == ["ComplexType", "EnumType"]
    assert options.generate_methods == "true"
    assert options.ignored_types == ["microsoft.graph.X", "microsoft.graph.Edu*"]
    assert options.routing == {"microsoft.graph.foo": "office365.foo"}
    assert options.type_routing == {"Bar*": "office365.bar"}


def test_missing_config_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="missing config"):
        GeneratorOptions.load("graph", tmp_path)


def test_unknown_top_level_key(tmp_path: Path) -> None:
    _write(tmp_path, _BASE + "bogus: 1\n")
    with pytest.raises(ConfigError, match="unknown key"):
        GeneratorOptions.load("graph", tmp_path)


def test_missing_required_key(tmp_path: Path) -> None:
    _write(tmp_path, "metadata_path: ./m.xml\n")
    with pytest.raises(ConfigError, match="missing required key 'output_path'"):
        GeneratorOptions.load("graph", tmp_path)


def test_unknown_filter_key(tmp_path: Path) -> None:
    _write(tmp_path, _BASE + "filters:\n  bogus: []\n")
    with pytest.raises(ConfigError, match="unknown filter key"):
        GeneratorOptions.load("graph", tmp_path)


def test_scanned_module_must_exist(tmp_path: Path) -> None:
    _write(tmp_path, _BASE.replace("modules: [office365]", "modules: [office365.missing]"))
    with pytest.raises(ConfigError, match="has no directory"):
        GeneratorOptions.load("graph", tmp_path)


def test_invalid_yaml(tmp_path: Path) -> None:
    _write(tmp_path, "metadata_path: [unclosed\n")
    with pytest.raises(ConfigError, match="invalid YAML"):
        GeneratorOptions.load("graph", tmp_path)


def test_parse_list_accepts_lists_strings_and_none() -> None:
    assert parse_list(["a", " b "]) == ["a", "b"]
    assert parse_list("a, b\nc") == ["a", "b", "c"]
    assert parse_list(None) == []


def test_split_ignored_separates_prefix_patterns() -> None:
    assert split_ignored(["X", "Edu*"]) == (["X"], ["Edu"])


def _load_strictly(path: Path) -> object:
    """Parse a settings file, refusing a mapping that repeats a key.

    ``yaml.safe_load`` keeps the *last* of two equal keys and says nothing, so a
    710-entry hand-maintained ``type_routing`` table can silently re-route a type by
    being edited twice. Two entries did exactly that (``AirPrintSettings`` and
    ``ArchivedPrintJob``, at ``office365.intune`` and ``office365.intune.print``).
    """
    import yaml

    class _Strict(yaml.SafeLoader):
        pass

    def construct_mapping(loader: yaml.SafeLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
        seen: set = set()
        for key_node, _ in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in seen:
                raise ValueError(f"duplicate key {key!r} at line {key_node.start_mark.line + 1}")
            seen.add(key)
        return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)

    _Strict.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_Strict)


@pytest.mark.parametrize("service", ["graph", "sharepoint"])
def test_the_settings_files_never_repeat_a_key(service: str) -> None:
    settings = Path(__file__).parents[2] / "generator" / f"settings.{service}.yaml"

    _load_strictly(settings)


def test_every_routed_type_names_a_package_module() -> None:
    settings = Path(__file__).parents[2] / "generator" / "settings.graph.yaml"
    routing = _load_strictly(settings)["type_routing"]

    wrong = {name: module for name, module in routing.items() if not str(module).startswith("office365.")}
    assert wrong == {}


# ------------------------------------------------------------------ BuilderContext


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
