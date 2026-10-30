"""A name every subtype declares is a name the base type carries.

SharePoint's v3 CSDL describes an object graph, not a list row: ``SP.ListItem`` declares
24 names and 147 per-list ``SP.Data.*Item`` types each declare the same 51 more, none of
which the base states. Those subtypes are filtered out of generation as per-list noise, so
before this rule the row reached the model only as hand-written getters -- 9 of 51.

The rule is measured, not assumed: :func:`intrinsic_members` promotes a name only when at
least :data:`MIN_SUBTYPES` subtypes agree on it, they agree on its type, the base does not
declare it, and it is not a navigation ($expand reaches a navigation through an entity
type; a base type that declares none has no wire path to invent).
"""

from __future__ import annotations

from pathlib import Path

from generator.config import GeneratorOptions
from generator.intrinsic_members import MIN_SUBTYPES, intrinsic_members
from generator.odata.v3.metadata_reader import ODataV3Reader
from generator.pipeline import GeneratorPipeline

_V3_HEADER = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="1.0" xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx">
  <edmx:DataServices>
    <Schema Namespace="SP" xmlns="http://schemas.microsoft.com/ado/2009/11/edm">
"""

_V3_FOOTER = """    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
"""

_BASE = """      <EntityType Name="Item">
        <Key><PropertyRef Name="Id" /></Key>
        <Property Name="Id" Type="Edm.Int32" Nullable="false" />
        <Property Name="Title" Type="Edm.String" />
      </EntityType>
"""


def _child(name: str, *properties: str) -> str:
    """A per-list type: it derives from ``SP.Item`` and adds ``properties``."""
    body = "".join(f'        <Property Name="{prop}" Type="Edm.String" />\n' for prop in properties)
    return (
        f'      <EntityType Name="Data.{name}" BaseType="SP.Item">\n'
        '        <Key><PropertyRef Name="Id" /></Key>\n'
        f"{body}"
        "      </EntityType>\n"
    )


def _model(tmp_path: Path, *types: str):
    schema = _V3_HEADER + _BASE + "".join(types) + _V3_FOOTER
    path = tmp_path / "metadata.xml"
    path.write_text(schema, encoding="utf-8")
    return ODataV3Reader(str(path)).read()


def test_a_name_every_subtype_declares_is_promoted_to_the_base(tmp_path: Path) -> None:
    """Three subtypes agree, so the column is on every instance the base addresses."""
    model = _model(
        tmp_path,
        _child("A", "RowFlag", "FileRef"),
        _child("B", "RowFlag", "FileRef"),
        _child("C", "RowFlag", "FileRef"),
    )

    promoted = intrinsic_members(model)

    assert list(promoted) == ["SP.Item"]
    # In the order the first subtype declares them, and with the type they agree on.
    assert [(prop.Name, prop.TypeName) for prop in promoted["SP.Item"]] == [
        ("RowFlag", "Edm.String"),
        ("FileRef", "Edm.String"),
    ]
    assert [prop.IsSystem for prop in promoted["SP.Item"]] == [True, True]


def test_a_coincidence_of_two_subtypes_is_not_promoted(tmp_path: Path) -> None:
    """At 2 subtypes ``SharePoint.xml`` promotes 179 names over 9 bases -- noise."""
    children = ("A", "B")
    model = _model(tmp_path, *(_child(name, "RowFlag") for name in children))

    assert len(children) < MIN_SUBTYPES, "the threshold is the measurement, not a formality"
    assert intrinsic_members(model) == {}


def test_a_name_the_base_declares_is_never_restated(tmp_path: Path) -> None:
    """``Title`` is the base's own fact; a second owner would be two declarations."""
    model = _model(
        tmp_path,
        _child("A", "Title", "RowFlag"),
        _child("B", "Title", "RowFlag"),
        _child("C", "Title", "RowFlag"),
    )

    assert [prop.Name for prop in intrinsic_members(model)["SP.Item"]] == ["RowFlag"]


def test_subtypes_that_disagree_about_the_type_are_refused(tmp_path: Path) -> None:
    """``OmaSetting.value`` is six types across seven subtypes: a guess, not a fact."""
    model = _model(
        tmp_path,
        _child("A", "Value"),
        _child("B", "Value"),
        _child("C", "Value"),
        """      <EntityType Name="Data.D" BaseType="SP.Item">
        <Key><PropertyRef Name="Id" /></Key>
        <Property Name="Value" Type="Edm.Int32" />
      </EntityType>
""",
    )

    assert intrinsic_members(model) == {}


def test_a_name_the_base_itself_declares_as_a_navigation_stays_out(tmp_path: Path) -> None:
    """$expand reaches a navigation; a base that declares none has no path to invent."""
    navigation = (
        '        <NavigationProperty Name="Owner" Relationship="SP.Item_Owner" ToRole="Owner" FromRole="Items" />\n'
    )
    children = "".join(
        f'      <EntityType Name="Data.{name}" BaseType="SP.Item">\n'
        '        <Key><PropertyRef Name="Id" /></Key>\n'
        '        <Property Name="RowFlag" Type="Edm.String" />\n'
        f"{navigation}"
        "      </EntityType>\n"
        for name in ("A", "B", "C")
    )
    model = _model(tmp_path, children)

    assert [prop.Name for prop in intrinsic_members(model)["SP.Item"]] == ["RowFlag"]


def test_the_generator_declares_a_promoted_member_as_system(tmp_path: Path) -> None:
    """``system=True`` is the provenance: the type's own CSDL never states this name."""
    model = _model(
        tmp_path,
        _child("A", "RowFlag"),
        _child("B", "RowFlag"),
        _child("C", "RowFlag"),
    )
    options = GeneratorOptions(
        metadata_path=str(tmp_path / "metadata.xml"),
        output_path=str(tmp_path / "office365"),
        modules="office365.runtime.types",
        namespace="SP",
        context_type="ClientContext",
        include_base_types=["EntityType"],
        generate_methods="false",
        routing={"SP": "office365"},
    )

    GeneratorPipeline(model, options, base_dir=tmp_path, force=True, smoke=False).run()

    source = (tmp_path / "office365" / "item.py").read_text(encoding="utf-8")
    assert '@odata(name="RowFlag", system=True)' in source
    # The base's own members keep the plain declaration: ``system`` is not contagious.
    assert '@odata(name="Title")' in source
    assert source.count("def row_flag") == 1
