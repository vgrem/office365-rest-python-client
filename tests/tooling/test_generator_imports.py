"""Offline tests for generated imports: the helpers that insert them, and the
navigation / TYPE_CHECKING / cycle placement that uses them."""

from __future__ import annotations

import ast
from pathlib import Path

from generator.builders.context import BuilderContext
from generator.builders.imports import (
    class_name_collides_with_import,
    drop_unused_type_checking,
    existing_import_names,
    insert_import,
    install_imports,
    make_import,
)
from generator.builders.type import TypeBuilder
from generator.odata.method import MethodInformation
from generator.odata.property import PropertyInformation
from generator.odata.type_information import TypeInformation
from office365.runtime.client_value import ClientValue


class _FixedResolver:
    """Resolves every type to one module (for import-placement tests)."""

    def __init__(self, module: str) -> None:
        self._module = module

    def resolve(self, type_name):
        return None

    def module_for(self, type_name):
        return self._module

    def strict_module_for(self, type_name, kind=None):
        return self._module

    def members_of(self, type_name):
        return set()


def _build_navigation_type(tmp_path: Path) -> str:
    schema = TypeInformation(BaseTypeFullName="EntityType", FullName="SP.TestFile", IsValueObject=False)
    schema.add_property(PropertyInformation(Name="Web", TypeName="SP.Web", IsNavigation=True))
    schema.add_property(PropertyInformation(Name="Versions", TypeName="Collection(SP.FileVersion)", IsNavigation=True))
    options = BuilderContext(output_path=str(tmp_path), modules="office365.sharepoint")
    builder = TypeBuilder(schema, options)
    builder.build()
    builder.save()
    return Path(builder.file).read_text(encoding="utf8")


def test_navigation_types_are_imported_lazily_and_under_type_checking(tmp_path: Path):
    source = _build_navigation_type(tmp_path)
    ast.parse(source)  # must be valid Python

    # annotation imports live under TYPE_CHECKING
    assert "if TYPE_CHECKING:" in source
    # runtime import inside the getter (module-level would cycle)
    assert "from office365.sharepoint.webs.web import Web" in source
    assert "from office365.sharepoint.files.versions.version import FileVersion" in source
    # both the annotation (TYPE_CHECKING) and the getter (local)
    assert source.count("from office365.sharepoint.webs.web import Web") == 2  # noqa: PLR2004

    # EntityCollection resolves to the SharePoint module, not the Graph one
    assert "from office365.sharepoint.entity_collection import EntityCollection" in source
    assert "from office365.entity_collection import EntityCollection" not in source


class _Value(ClientValue):
    """A stand-in for a generated complex value type."""


class _ValueResolver(_FixedResolver):
    """Resolves every custom type to a value class, so it is not a navigation."""

    def resolve(self, type_name):
        return _Value


def test_a_value_typed_entity_getter_declares_its_type_at_runtime(tmp_path: Path):
    """A getter that constructs its value needs the name at module level.

    The return annotation is read at run time to decide how to hydrate a payload
    (``declared_type``); a name that exists only under ``if TYPE_CHECKING:``
    raises NameError there, so the column resolved to no type at all and
    ``set_property`` stored a bare dict where the model promises a value object.
    """
    schema = TypeInformation(BaseTypeFullName="EntityType", FullName="SP.TestEvent", IsValueObject=False)
    schema.add_property(PropertyInformation(Name="start", TypeName="SP.DateValue"))
    options = BuilderContext(output_path=str(tmp_path), modules="office365.sharepoint")
    builder = TypeBuilder(schema, options, resolver=_ValueResolver("office365.sharepoint.date_value"))
    builder.build()
    source = builder.render()
    ast.parse(source)

    import_line = "from office365.sharepoint.date_value import DateValue"
    assert source.count(import_line) == 1  # module level, and not repeated in the getter
    assert "def start(self) -> DateValue:" in source
    assert "if TYPE_CHECKING:" not in source


def test_complex_value_collection_does_not_emit_bracketed_import(tmp_path: Path):
    """A ClientValue collection imports the wrapper and item type, not ``CVC[X]``."""
    schema = TypeInformation(BaseTypeFullName="EntityType", FullName="SP.TestThing", IsValueObject=False)
    schema.add_property(PropertyInformation(Name="Entries", TypeName="Collection(SP.ResourceEntry)"))
    options = BuilderContext(output_path=str(tmp_path), modules="office365.sharepoint")
    builder = TypeBuilder(schema, options)
    builder.build()
    source = builder.render()
    ast.parse(source)
    assert [line for line in source.splitlines() if line.startswith("from ") and "[" in line] == []


def test_client_value_field_type_is_a_runtime_import(tmp_path: Path):
    """A dataclass field's ``default_factory=X`` needs X at runtime, not only under TYPE_CHECKING."""
    schema = TypeInformation(BaseTypeFullName="ComplexType", FullName="microsoft.graph.TestValue", IsValueObject=True)
    schema.add_property(PropertyInformation(Name="Subject", TypeName="microsoft.graph.WorkflowSubject"))
    options = BuilderContext(context_type="GraphClient", output_path=str(tmp_path), modules="office365")
    builder = TypeBuilder(schema, options, resolver=_FixedResolver("office365.workflow_subject"))
    builder.build()
    source = builder.render()
    ast.parse(source)

    lines = source.splitlines()
    import_line = "from office365.workflow_subject import WorkflowSubject"
    runtime_index = lines.index(import_line)
    type_checking_index = next((i for i, line in enumerate(lines) if line.startswith("if TYPE_CHECKING:")), len(lines))
    assert runtime_index < type_checking_index  # module-level, before the TYPE_CHECKING block


def test_dataclass_member_named_field_aliases_the_dataclasses_field_import(tmp_path: Path):
    """A member named ``field`` must not shadow ``dataclasses.field`` used by later fields."""
    schema = TypeInformation(BaseTypeFullName="ComplexType", FullName="microsoft.graph.TestOption", IsValueObject=True)
    schema.add_property(PropertyInformation(Name="field", TypeName="Edm.String"))
    schema.add_property(PropertyInformation(Name="bucket", TypeName="microsoft.graph.Bucket"))
    options = BuilderContext(context_type="GraphClient", output_path=str(tmp_path), modules="office365")
    builder = TypeBuilder(schema, options, resolver=_FixedResolver("office365.bucket"))
    builder.build()
    source = builder.render()
    ast.parse(source)

    assert "from dataclasses import field as field_" in source
    assert "field_(default_factory=Bucket)" in source
    assert "field: str | None = None" in source


def test_entity_field_in_a_client_value_defaults_to_none(tmp_path: Path):
    """An entity field needs a context, so inside a ClientValue it defaults to None."""
    schema = TypeInformation(BaseTypeFullName="ComplexType", FullName="microsoft.graph.TestValue", IsValueObject=True)
    schema.add_property(PropertyInformation(Name="owner", TypeName="microsoft.graph.SomeEntity"))
    options = BuilderContext(
        context_type="GraphClient",
        output_path=str(tmp_path),
        modules="office365",
        entity_types=frozenset({"microsoft.graph.SomeEntity"}),
    )
    builder = TypeBuilder(schema, options, resolver=_FixedResolver("office365.some_entity"))
    builder.build()
    source = builder.render()
    ast.parse(source)

    assert "owner: SomeEntity | None = None" in source
    assert "default_factory=SomeEntity" not in source


def test_method_entity_return_is_imported_lazily(tmp_path: Path):
    """A bound function returning an entity imports it under TYPE_CHECKING + locally."""
    schema = TypeInformation(BaseTypeFullName="EntityType", FullName="SP.TestThing", IsValueObject=False)
    schema.add_method(
        MethodInformation(
            Name="GetWeb",
            ReturnTypeFullName="SP.Web",
            BindingTypeFullName="SP.TestThing",
            IsBound=True,
            IsStatic=False,
            Kind="function",
        )
    )
    options = BuilderContext(output_path=str(tmp_path), modules="office365.sharepoint", generate_methods="true")
    builder = TypeBuilder(schema, options)
    builder.build()
    source = builder.render()
    ast.parse(source)
    assert "def get_web" in source
    assert source.count("from office365.sharepoint.webs.web import Web") == 2  # noqa: PLR2004


# ---------------------------------------------------------------- import helpers


def test_existing_import_names_includes_type_checking_block() -> None:
    tree = ast.parse("from a import A\nimport b\nif TYPE_CHECKING:\n    from c import C\n")

    assert existing_import_names(tree) == {"A", "b", "C"}


def test_insert_import_keeps_only_missing_names() -> None:
    tree = ast.parse("from a import A\n")
    existing = existing_import_names(tree)

    assert insert_import(tree, ast.parse("from a import A, B").body[0], existing, len(tree.body))
    assert ast.unparse(tree.body[-1]) == "from a import B"


def test_insert_import_preserves_alias() -> None:
    tree = ast.parse("")

    assert insert_import(tree, ast.parse("from dataclasses import field as field_").body[0], set(), 0)
    assert ast.unparse(tree.body[0]) == "from dataclasses import field as field_"


def test_install_imports_skips_already_present_names() -> None:
    tree = ast.parse("import os\n")
    existing = existing_import_names(tree)
    references = [ast.parse("import os").body[0], ast.parse("import sys").body[0]]

    inserted = install_imports(tree, references, existing, len(tree.body))

    assert [ast.unparse(node) for node in inserted] == ["import sys"]


def test_drop_unused_type_checking_removes_empty_block() -> None:
    tree = ast.parse("from typing import TYPE_CHECKING\n\n\nclass A:\n    pass\n")
    added = [tree.body[0]]

    kept = drop_unused_type_checking(tree, added)

    assert kept == []
    assert not any(isinstance(node, ast.ImportFrom) and node.module == "typing" for node in tree.body)


def test_drop_unused_type_checking_keeps_a_used_block() -> None:
    tree = ast.parse("from typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    from a import A\n")
    added = [tree.body[0]]

    assert drop_unused_type_checking(tree, added) == added
    assert any(isinstance(node, ast.If) for node in tree.body)


def test_class_name_collides_with_import() -> None:
    tree = ast.parse("from a import Thing\n")

    assert class_name_collides_with_import(tree, "Thing")
    assert not class_name_collides_with_import(tree, "Other")


def test_make_import_sorts_names() -> None:
    assert ast.unparse(make_import("a", ["b", "a"])) == "from a import a, b"
