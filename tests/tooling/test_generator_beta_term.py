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

import ast
import importlib.util
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

_REPO_ROOT = Path(__file__).resolve().parents[2]


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


# --------------------------------------------------------------------------- planning


def _codemod():
    """``scripts/mark_odata.py``, imported by path: it is a script, not a package."""
    spec = importlib.util.spec_from_file_location("_mark_odata", _REPO_ROOT / "scripts" / "mark_odata.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _planned(tmp_path: Path, source: str, declared: object, *, only: set[str] | None = None) -> list[str]:
    """The lines the codemod would insert, given what the catalog says about one member."""
    module = tmp_path / "gadget.py"
    module.write_text(source, encoding="utf-8")
    tree = ast.parse(source)
    node = next(child for child in tree.body if isinstance(child, ast.ClassDef))
    edits = _codemod().pending_markers(tree, node, {"Value": declared}, source.splitlines(keepends=True), only=only)
    return [edit.new.strip() for edit in edits]


_GETTER = """
from office365.runtime.types.odata_property import odata


class Gadget(Entity):
    @odata(name="Value")
    @property
    def value(self):
        return self.properties.get("Value", None)
"""


def test_a_member_the_preview_alone_declares_is_finished_with_beta(tmp_path: Path) -> None:
    declared = _codemod().Declared(name="Value", navigation=False, enum=False, beta=True)

    # One keyword on the line that is already there: the declaration is a statement about
    # the member, and the back-fill only adds the fact the snapshot supplies.
    assert _planned(tmp_path, _GETTER, declared) == ['@odata(name="Value", beta=True)']
    # ``--only beta`` leaves every other missing fact alone, which is how the back-fill
    # lands without also rewriting 8,593 unrelated Graph lines.
    assert _planned(tmp_path, _GETTER, declared, only={"beta"}) == ['@odata(name="Value", beta=True)']
    stable = _codemod().Declared(name="Value", navigation=False, enum=False)
    assert _planned(tmp_path, _GETTER, stable) == []


def test_a_preview_type_owns_the_fact_its_members_do_not_repeat_it(tmp_path: Path) -> None:
    """962 of the document's 1,401 member marks sit inside a preview type; they add nothing."""
    model = ODataV3Reader(str(_metadata(tmp_path))).read()

    catalog = _codemod()._catalog_of(model)

    assert catalog["sp.widget"]["PreviewOnly"].beta, "a stable type's preview member is marked"
    assert not catalog["sp.gadget"]["Name"].beta, "the type carries it; the member does not repeat it"
