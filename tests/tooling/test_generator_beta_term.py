"""The preview surface of a single-document service is read, not inferred.

SharePoint ships one v3 document for both the stable and the preview surface, and states
the difference with ``Com.Microsoft.VisualStudio.CodeGen.IsBeta`` on a schema-level
annotation block: a target naming a type marks the type, a target naming ``Type/member``
marks one member of a type that is otherwise stable. Graph needs none of this -- its
preview is a second document, and the two snapshots are diffed instead -- so the term is
the only way a v3 tree can know.

Nothing here touches a network: the CSDL is a few dozen lines of XML.
"""

from __future__ import annotations

from pathlib import Path

from generator.odata.csdl import CsdlDocument
from generator.odata.v3.metadata_reader import ODataV3Reader

_V3_HEADER = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="1.0" xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx">
  <edmx:DataServices>
    <Schema Namespace="SP" xmlns="http://schemas.microsoft.com/ado/2009/11/edm">
"""

_V3_FOOTER = """    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
"""

_BETA_TERM = "Com.Microsoft.VisualStudio.CodeGen.IsBeta"

_TYPES = """      <EntityType Name="Widget">
        <Key><PropertyRef Name="Id" /></Key>
        <Property Name="Id" Type="Edm.Int32" Nullable="false" />
        <Property Name="Name" Type="Edm.String" />
        <Property Name="PreviewOnly" Type="Edm.String" />
      </EntityType>
      <EntityType Name="Gadget">
        <Key><PropertyRef Name="Id" /></Key>
        <Property Name="Id" Type="Edm.Int32" Nullable="false" />
        <Property Name="Name" Type="Edm.String" />
      </EntityType>
"""

_ANNOTATIONS = f"""      <Annotations Target="SP.Gadget">
        <ValueAnnotation Term="{_BETA_TERM}" Bool="true" />
      </Annotations>
      <Annotations Target="SP.Gadget/Name">
        <ValueAnnotation Term="{_BETA_TERM}" Bool="true" />
      </Annotations>
      <Annotations Target="SP.Widget/PreviewOnly">
        <ValueAnnotation Term="{_BETA_TERM}" Bool="true" />
      </Annotations>
      <Annotations Target="SP.Widget/Name">
        <ValueAnnotation Term="{_BETA_TERM}" Bool="false" />
      </Annotations>
      <Annotations Target="SP.Widget/Id">
        <ValueAnnotation Term="Org.OData.Core.V1.Computed" Bool="true" />
      </Annotations>
      <Annotations Target="SP.Api/Call(SP.Widget)">
        <ValueAnnotation Term="{_BETA_TERM}" Bool="true" />
      </Annotations>
"""

_NAMESPACES = {
    "xmlns": "http://schemas.microsoft.com/ado/2009/11/edm",
    "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
}


def _metadata(tmp_path: Path, annotations: str = _ANNOTATIONS) -> Path:
    path = tmp_path / "metadata.xml"
    path.write_text(_V3_HEADER + _TYPES + annotations + _V3_FOOTER, encoding="utf-8")
    return path


def test_a_bare_target_marks_a_type_and_a_slashed_one_a_member(tmp_path: Path) -> None:
    document = CsdlDocument.load(str(_metadata(tmp_path)), _NAMESPACES)

    # The function import carries the term too (1,222 of the real ones do), and a target
    # that names a call is not a type: it is dropped rather than spelled as one.
    assert document.parse_beta_types() == {"SP.Gadget"}
    assert document.parse_beta_members() == {("SP.Gadget", "Name"), ("SP.Widget", "PreviewOnly")}


def test_the_v4_carrier_states_the_same_fact(tmp_path: Path) -> None:
    """``<Annotation>`` instead of ``<ValueAnnotation>``: one term, two dialects."""
    document = CsdlDocument.load(
        str(_metadata(tmp_path, _ANNOTATIONS.replace("ValueAnnotation", "Annotation"))), _NAMESPACES
    )

    assert document.parse_beta_types() == {"SP.Gadget"}
    assert document.parse_beta_members() == {("SP.Gadget", "Name"), ("SP.Widget", "PreviewOnly")}


def test_the_model_carries_the_fact_per_type_and_per_member(tmp_path: Path) -> None:
    model = ODataV3Reader(str(_metadata(tmp_path))).read()

    gadget = model.types["SP.Gadget"]
    assert gadget.IsBeta, "a type the document marks is preview"
    assert gadget.Properties["Name"].IsBeta, "the document marks the member as well"

    widget = model.types["SP.Widget"]
    assert not widget.IsBeta, "a stable type stays stable"
    assert widget.Properties["PreviewOnly"].IsBeta, "one preview member does not make the type preview"
    assert not widget.Properties["Name"].IsBeta, "Bool='false' is not a mark"
    assert not widget.Properties["Id"].IsBeta, "a block carrying another term says nothing about beta"
