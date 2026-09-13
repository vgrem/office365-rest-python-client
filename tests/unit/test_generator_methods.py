"""Offline tests for generated OData operation methods (functions/actions)."""

from __future__ import annotations

import ast
import textwrap
from pathlib import Path

from generator.builders.method import MethodBuilder
from office365.runtime.odata.method import MethodInformation
from office365.runtime.odata.v3.metadata_reader import ODataV3Reader
from office365.runtime.odata.v4.metadata_reader import ODataV4Reader

_V3_METADATA = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx">
  <edmx:DataServices>
    <Schema Namespace="SP" xmlns="http://schemas.microsoft.com/ado/2009/11/edm">
      <EntityType Name="ObjectSharingInformation">
        <Key><PropertyRef Name="AnonymousEditLink"/></Key>
        <Property Name="AnonymousEditLink" Type="Edm.String" Nullable="false"/>
      </EntityType>
      <EntityContainer Name="ApiData">
        <FunctionImport Name="SP_ObjectSharingInformation_CanCurrentUserShareRemote" ReturnType="Edm.Int32">
          <Parameter Name="docId" Type="Edm.String"/>
        </FunctionImport>
        <FunctionImport Name="MoveToSecondStage" IsBindable="true">
          <Parameter Name="this" Type="SP.ObjectSharingInformation"/>
        </FunctionImport>
        <FunctionImport
          Name="ObjectSharingInformationSet"
          ReturnType="Collection(SP.ObjectSharingInformation)"
          EntitySet="ObjectSharingInformations"/>
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
"""

_V4_METADATA = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema Namespace="microsoft.graph.identityGovernance" xmlns="http://docs.oasis-open.org/odata/ns/edm">
      <EntityType Name="workflow">
        <Key><PropertyRef Name="id"/></Key>
        <Property Name="id" Type="Edm.String" Nullable="false"/>
      </EntityType>
      <Action Name="activate" IsBound="true">
        <Parameter Name="bindingParameter" Type="microsoft.graph.identityGovernance.workflow"/>
      </Action>
      <Action Name="clearQuarantine" IsBound="true">
        <Parameter Name="bindingParameter" Type="microsoft.graph.identityGovernance.workflow"/>
        <ReturnType Type="microsoft.graph.identityGovernance.workflow"/>
      </Action>
      <Function Name="summary" IsBound="true">
        <Parameter Name="bindingParameter" Type="Collection(microsoft.graph.identityGovernance.workflow)"/>
        <Parameter Name="startDateTime" Type="Edm.DateTimeOffset" Nullable="false"/>
        <ReturnType Type="microsoft.graph.identityGovernance.workflow"/>
      </Function>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
"""


def _write(tmp_path: Path, name: str, content: str) -> str:
    path = tmp_path / name
    path.write_text(textwrap.dedent(content), encoding="utf8")
    return str(path)


def test_v3_parses_bound_and_static_function_imports(tmp_path: Path):
    model = ODataV3Reader(_write(tmp_path, "sp.xml", _V3_METADATA)).generate_model()
    schema = model.types["SP.ObjectSharingInformation"]

    static = schema.Methods["CanCurrentUserShareRemote"]
    assert static.IsStatic is True
    assert static.Kind == "action"
    assert static.ReturnTypeFullName == "Edm.Int32"
    assert [p["Name"] for p in static.Parameters] == ["docId"]

    bound = schema.Methods["MoveToSecondStage"]
    assert bound.IsStatic is False
    assert bound.IsBound is True
    assert bound.Kind == "action"
    assert bound.Parameters == []

    # entity-set accessors are skipped
    assert "ObjectSharingInformationSet" not in schema.Methods


def test_v4_parses_bound_actions_and_functions(tmp_path: Path):
    model = ODataV4Reader(_write(tmp_path, "graph.xml", _V4_METADATA)).generate_model()
    schema = model.types["microsoft.graph.identityGovernance.Workflow"]

    activate = schema.Methods["activate"]
    assert activate.Kind == "action"
    assert activate.IsBound is True
    assert activate.ReturnTypeFullName is None

    quarantine = schema.Methods["clearQuarantine"]
    assert quarantine.ReturnTypeFullName == "microsoft.graph.identityGovernance.workflow"

    summary = schema.Methods["summary"]
    assert summary.Kind == "function"
    assert [p["Name"] for p in summary.Parameters] == ["startDateTime"]


def _compile(source: str) -> ast.Module:
    return ast.parse(source)


def test_method_builder_static_function():
    schema = MethodInformation(
        Name="CanCurrentUserShareRemote",
        Parameters=[{"Name": "docId", "Type": "Edm.String", "Nullable": True}],
        ReturnTypeFullName="Edm.Int32",
        BindingTypeFullName="SP.ObjectSharingInformation",
        IsBound=False,
        IsStatic=True,
        Kind="action",
    )
    source = MethodBuilder(schema).build_source()

    assert "@staticmethod" in source
    assert "def can_current_user_share_remote(context, doc_id: str) -> ClientResult[int]:" in source
    assert "ServiceOperationQuery(" in source
    assert "None, return_type, True" in source  # is_static
    _compile(source)


def test_method_builder_instance_void_and_primitive():
    void = MethodInformation(
        Name="MoveToSecondStage",
        BindingTypeFullName="SP.ObjectSharingInformation",
        IsBound=True,
        IsStatic=False,
        Kind="action",
    )
    source = MethodBuilder(void).build_source()
    assert "def move_to_second_stage(self) -> Self:" in source
    assert "return self" in source
    _compile(source)

    primitive = MethodInformation(
        Name="CanCurrentUserShare",
        Parameters=[{"Name": "docId", "Type": "Edm.String", "Nullable": True}],
        ReturnTypeFullName="Edm.Int32",
        BindingTypeFullName="SP.ObjectSharingInformation",
        IsBound=True,
        IsStatic=False,
        Kind="function",
    )
    source = MethodBuilder(primitive).build_source()
    assert "-> ClientResult[int]:" in source
    assert "FunctionQuery(self" in source
    _compile(source)
