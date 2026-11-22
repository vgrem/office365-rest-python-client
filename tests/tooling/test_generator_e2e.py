"""The generator end to end, one test per step a run takes.

* CSDL is read into a type model: keys, properties, members, navigations, operations.
* An EDM type becomes the Python type it maps to on the generated class.
* The model is rendered as entity, complex and enum classes, with their getters,
  bound actions and functions.
* A run against changed metadata is a diff: what the metadata gained is written, what
  a person wrote stays, what the metadata dropped is reported and kept in code.

Every generated module is ``ast.parse``d, so source that does not compile fails here
rather than on the next import.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

from generator.core.config import GeneratorOptions
from generator.odata.v3.metadata_reader import ODataV3Reader
from generator.odata.v4.metadata_reader import ODataV4Reader
from generator.pipeline import GeneratorPipeline

_V3_CSDL = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="1.0" xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx">
  <edmx:DataServices>
    <Schema Namespace="SP" xmlns="http://schemas.microsoft.com/ado/2009/11/edm">
      <EnumType Name="WidgetKind">
        <Member Name="alpha" Value="0" />
        <Member Name="beta" Value="1" />
      </EnumType>
      <ComplexType Name="WidgetSettings">
        <Property Name="name" Type="Edm.String" />
        <Property Name="kind" Type="SP.WidgetKind" />
      </ComplexType>
      <EntityType Name="Widget">
        <Key><PropertyRef Name="Id" /></Key>
        <Property Name="Id" Type="Edm.String" Nullable="false" />
        <Property Name="Title" Type="Edm.String" />
      </EntityType>
      <FunctionImport Name="DoThing" ReturnType="Edm.String" IsBindable="true" IsComposable="true">
        <Parameter Name="this" Type="SP.Widget" />
        <Parameter Name="count" Type="Edm.Int32" />
      </FunctionImport>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
"""

_V4_CSDL = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema Namespace="microsoft.graph" xmlns="http://docs.oasis-open.org/odata/ns/edm">
      <EnumType Name="WidgetKind">
        <Member Name="alpha" Value="0" />
        <Member Name="beta" Value="1" />
      </EnumType>
      <ComplexType Name="WidgetSettings">
        <Property Name="kind" Type="microsoft.graph.WidgetKind" />
      </ComplexType>
      <EntityType Name="Widget">
        <Key><PropertyRef Name="id" /></Key>
        <Property Name="id" Type="Edm.String" Nullable="false" />
        <NavigationProperty Name="widgets" Type="Collection(microsoft.graph.Widget)" ContainsTarget="true" />
      </EntityType>
      <Action Name="reset" IsBound="true">
        <Parameter Name="bindingParameter" Type="microsoft.graph.Widget" />
        <Parameter Name="reason" Type="Edm.String" />
      </Action>
      <Function Name="findWidgets" IsBound="true" IsComposable="true">
        <Parameter Name="bindingParameter" Type="microsoft.graph.Widget" />
        <Parameter Name="startDateTime" Type="Edm.String" />
        <Parameter Name="returnType" Type="Edm.String" />
        <ReturnType Type="Collection(microsoft.graph.Widget)" />
      </Function>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
"""

#: Every primitive this project maps, plus a collection, an enum and a complex type.
_TYPES_CSDL = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema Namespace="microsoft.graph" xmlns="http://docs.oasis-open.org/odata/ns/edm">
      <EnumType Name="WidgetKind">
        <Member Name="alpha" Value="0" />
      </EnumType>
      <ComplexType Name="WidgetSettings">
        <Property Name="kind" Type="microsoft.graph.WidgetKind" />
      </ComplexType>
      <EntityType Name="Widget">
        <Key><PropertyRef Name="id" /></Key>
        <Property Name="id" Type="Edm.String" Nullable="false" />
        <Property Name="count" Type="Edm.Int32" />
        <Property Name="enabled" Type="Edm.Boolean" />
        <Property Name="weight" Type="Edm.Double" />
        <Property Name="created" Type="Edm.DateTimeOffset" />
        <Property Name="guid" Type="Edm.Guid" />
        <Property Name="tags" Type="Collection(Edm.String)" />
        <Property Name="settings" Type="microsoft.graph.WidgetSettings" />
        <NavigationProperty Name="widgets" Type="Collection(microsoft.graph.Widget)" />
      </EntityType>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
"""

_COMPUTED_CSDL = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema Namespace="microsoft.graph" xmlns="http://docs.oasis-open.org/odata/ns/edm">
      <EntityType Name="Widget">
        <Key><PropertyRef Name="id" /></Key>
        <Property Name="id" Type="Edm.String" Nullable="false" />
        <Property Name="subject" Type="Edm.String" />
        <NavigationProperty Name="owner" Type="Collection(microsoft.graph.Widget)" />
      </EntityType>
      <Annotations Target="microsoft.graph.Widget/id">
        <Annotation Term="Org.OData.Core.V1.Computed" Bool="true" />
      </Annotations>
      <Annotations Target="microsoft.graph.Widget/owner">
        <Annotation Term="Org.OData.Core.V1.Computed" Bool="true" />
      </Annotations>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
"""

_CUSTOM_METHOD = '''
    def custom_method(self, value):
        """Hand-written: must survive regeneration."""
        return self.get_property("subject", value)
'''


def _options(tmp_path: Path, *, graph: bool, namespace: str, kinds: list[str], prefix: str) -> GeneratorOptions:
    """Options for the fixture run. ``graph`` picks the seed base class, as the config does."""
    return GeneratorOptions(
        metadata_path=str(tmp_path / "metadata.xml"),
        output_path=str(tmp_path / "office365"),
        modules="office365.runtime.types",
        namespace=namespace,
        context_type="GraphClient" if graph else "ClientContext",
        include_base_types=kinds,
        generate_methods="true",
        routing={prefix: "office365"},
    )


def _run(options: GeneratorOptions, reader: type, tmp_path: Path, *, force: bool = False, **extra) -> int:
    model = reader(options.metadata_path).read()
    return GeneratorPipeline(model, options, base_dir=tmp_path, force=force, smoke=False, **extra).run()


def _source(tmp_path: Path, name: str) -> str:
    source = (tmp_path / "office365" / name).read_text(encoding="utf-8")
    ast.parse(source)
    return source


def _graph_options(tmp_path: Path, kinds: list[str]) -> GeneratorOptions:
    return _options(tmp_path, graph=True, namespace="", kinds=kinds, prefix="microsoft.graph")


# --- 1. CSDL is read into the model -------------------------------------------------


def test_both_readers_parse_csdl_into_the_type_model(tmp_path: Path) -> None:
    """The document's facts, read off the model — no source involved yet."""
    (tmp_path / "metadata.xml").write_text(_V3_CSDL, encoding="utf-8")
    v3 = ODataV3Reader(str(tmp_path / "metadata.xml")).read()

    widget = v3.get_type("SP.Widget")
    assert widget.Key == ("Id",)
    assert [(name, prop.TypeName) for name, prop in widget.Properties.items()] == [
        ("Id", "Edm.String"),
        ("Title", "Edm.String"),
    ]
    assert sorted(v3.get_type("SP.WidgetKind").Members) == ["alpha", "beta"]
    do_thing = widget.Methods["DoThing"]
    assert (do_thing.Kind, do_thing.IsBound, do_thing.BindingTypeFullName) == ("function", True, "SP.Widget")
    assert do_thing.ReturnTypeFullName == "Edm.String"  # the binding parameter is not a parameter

    (tmp_path / "metadata.xml").write_text(_V4_CSDL, encoding="utf-8")
    v4 = ODataV4Reader(str(tmp_path / "metadata.xml")).read()

    widget = v4.get_type("microsoft.graph.Widget")
    assert widget.Key == ("id",)
    assert widget.Properties["widgets"].IsNavigation is True
    assert widget.Methods["reset"].Kind == "action"
    find = widget.Methods["findWidgets"]
    assert find.Kind == "function"
    assert find.ReturnTypeFullName == "Collection(microsoft.graph.Widget)"
    assert [param["Name"] for param in find.Parameters] == ["startDateTime", "returnType"]


# --- 2. EDM types become Python types -----------------------------------------------


def test_an_edm_type_becomes_the_python_type_it_maps_to(tmp_path: Path) -> None:
    (tmp_path / "metadata.xml").write_text(_TYPES_CSDL, encoding="utf-8")
    _run(_graph_options(tmp_path, ["EntityType", "ComplexType", "EnumType"]), ODataV4Reader, tmp_path)

    source = _source(tmp_path, "widget.py")
    for annotation in (
        "def count(self) -> Optional[int]:",
        "def enabled(self) -> Optional[bool]:",
        "def weight(self) -> Optional[float]:",
        "def created(self) -> Optional[datetime]:",
        "def guid(self) -> Optional[UUID]:",
        "def tags(self) -> StringCollection:",
        "def settings(self) -> Optional[WidgetSettings]:",
        "def widgets(self) -> EntityCollection[Widget]:",
    ):
        assert annotation in source
    assert "kind: WidgetKind = WidgetKind.alpha" in _source(tmp_path, "widget_settings.py")  # enum default
    assert 'alpha = "0"' in _source(tmp_path, "widget_kind.py")  # members keep their wire value


# --- 3. Types, methods and properties are generated ---------------------------------


def test_sharepoint_renders_an_entity_complex_and_enum_with_its_function(tmp_path: Path) -> None:
    (tmp_path / "metadata.xml").write_text(_V3_CSDL, encoding="utf-8")
    kinds = ["EntityType", "ComplexType", "EnumType"]
    _run(_options(tmp_path, graph=False, namespace="SP", kinds=kinds, prefix="SP"), ODataV3Reader, tmp_path)

    entity = _source(tmp_path, "widget.py")
    assert "class Widget(Entity):" in entity
    assert "def do_thing" in entity  # a bound FunctionImport becomes a method
    # Every generated getter carries its OData name, so no caller spells it again.
    assert '@odata(name="Title")' in entity
    assert "from office365.runtime.types.odata_property import odata" in entity
    assert "class WidgetSettings(ClientValue):" in _source(tmp_path, "widget_settings.py")
    assert "class WidgetKind(Enum):" in _source(tmp_path, "widget_kind.py")


def test_graph_renders_a_navigation_and_bound_operations(tmp_path: Path) -> None:
    (tmp_path / "metadata.xml").write_text(_V4_CSDL, encoding="utf-8")
    kinds = ["EntityType", "ComplexType", "EnumType"]
    _run(_graph_options(tmp_path, kinds), ODataV4Reader, tmp_path)

    entity = _source(tmp_path, "widget.py")
    # The wire name is declared exactly once, by the property the runtime reads.
    assert 'def entity_type_name(self) -> str:\n        return "microsoft.graph.Widget"' in entity
    assert "_odata_type_name" not in entity
    assert "def reset" in entity  # a bound Action
    # Graph matches a function's parameters by name; an unnamed list reads as a
    # navigation property to the service.
    assert '{"startDateTime": start_date_time, "returnType": return_type},' in entity
    # A parameter called returnType must not take the returned object's place.
    assert "return_type_ = EntityCollection(self.context, Widget)" in entity
    assert "return return_type_" in entity
    # A navigation property is declared as such: $expand reaches it, $select cannot.
    assert '@odata(name="widgets", navigation=True)' in entity


def test_a_computed_member_is_generated_read_only(tmp_path: Path) -> None:
    """Graph states this one level above the property, which the property node cannot see."""
    (tmp_path / "metadata.xml").write_text(_COMPUTED_CSDL, encoding="utf-8")
    _run(_graph_options(tmp_path, ["EntityType"]), ODataV4Reader, tmp_path)

    entity = _source(tmp_path, "widget.py")
    assert '@odata(name="id", readonly=True)' in entity
    assert '@odata(name="subject")' in entity  # neither computed nor a navigation: declared plainly
    assert '@odata(name="owner", navigation=True, readonly=True)' in entity


# --- 4. A run is a diff -------------------------------------------------------------


def test_a_second_run_on_the_same_metadata_writes_nothing(tmp_path: Path) -> None:
    (tmp_path / "metadata.xml").write_text(_V4_CSDL, encoding="utf-8")
    options = _graph_options(tmp_path, ["EntityType", "ComplexType", "EnumType"])
    _run(options, ODataV4Reader, tmp_path)
    entity = _source(tmp_path, "widget.py")

    assert _run(options, ODataV4Reader, tmp_path) == 0  # the manifest answers before any build
    _run(options, ODataV4Reader, tmp_path, force=True)
    assert _source(tmp_path, "widget.py") == entity


def test_an_update_adds_what_is_new_and_keeps_what_a_person_wrote(tmp_path: Path) -> None:
    metadata = tmp_path / "metadata.xml"
    metadata.write_text(_V4_CSDL, encoding="utf-8")
    options = _graph_options(tmp_path, ["EntityType", "ComplexType", "EnumType"])
    _run(options, ODataV4Reader, tmp_path)

    widget = tmp_path / "office365" / "widget.py"
    widget.write_text(widget.read_text(encoding="utf-8").rstrip("\n") + "\n" + _CUSTOM_METHOD, encoding="utf-8")

    # The metadata gains a property and a type, and drops a navigation and a type.
    metadata.write_text(
        _V4_CSDL.replace(
            '<NavigationProperty Name="widgets" Type="Collection(microsoft.graph.Widget)" ContainsTarget="true" />',
            '<Property Name="subject" Type="Edm.String" />',
        )
        .replace(
            '      <ComplexType Name="WidgetSettings">\n'
            '        <Property Name="kind" Type="microsoft.graph.WidgetKind" />\n'
            "      </ComplexType>\n",
            "",
        )
        .replace(
            "    </Schema>",
            '      <EntityType Name="Gadget">\n'
            '        <Key><PropertyRef Name="id" /></Key>\n'
            '        <Property Name="id" Type="Edm.String" Nullable="false" />\n'
            "      </EntityType>\n"
            "    </Schema>",
        ),
        encoding="utf-8",
    )
    report = tmp_path / "run.json"
    _run(options, ODataV4Reader, tmp_path, report_path=str(report))

    # What the metadata gained is written: the new getter, the new type's module.
    entity = _source(tmp_path, "widget.py")
    assert '@odata(name="subject")' in entity
    assert "def custom_method(self, value):" in entity  # and what a person wrote stays
    assert (tmp_path / "office365" / "gadget.py").is_file()
    # What the metadata dropped is reported once and kept in code, not deleted.
    changes = json.loads(report.read_text(encoding="utf-8"))
    assert changes["created"] == ["microsoft.graph.Gadget"]
    assert "microsoft.graph.Widget" in changes["updated"]
    assert changes["removed_types"] == ["microsoft.graph.WidgetSettings"]
    assert changes["removed_members"] == {"microsoft.graph.Widget": ["widgets"]}
    assert (tmp_path / "office365" / "widget_settings.py").is_file()
    assert '@odata(name="widgets", navigation=True)' in entity  # the dropped getter still answers
