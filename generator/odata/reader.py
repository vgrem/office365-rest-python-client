from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Optional
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from office365.runtime.odata.type import ODataType

from generator.odata.member import MemberInformation
from generator.odata.method import MethodInformation
from generator.odata.model import ODataModel
from generator.odata.property import PropertyInformation
from generator.odata.type_information import TypeInformation

_BASE_TYPES = ("ComplexType", "EntityType", "EnumType")


class ODataReader(ABC):
    """Parses OData CSDL metadata into an :class:`ODataModel`."""

    def __init__(self, metadata_path: str):
        self._metadata_path = metadata_path
        self._root: Optional[Element] = None

    @property
    @abstractmethod
    def xml_namespaces(self) -> Dict[str, str]:
        """XML namespaces for the specific OData version"""

    def read(self) -> ODataModel:
        """Parses the metadata file and returns the populated model."""
        model = ODataModel()
        self._root = ET.parse(self._metadata_path).getroot()
        self._parse_types(model)
        self.process_operations(model)
        return model

    def _parse_types(self, model: ODataModel) -> None:
        assert self._root is not None
        schema_nodes = self._root.findall("edmx:DataServices/xmlns:Schema", self.xml_namespaces)
        for base_type in _BASE_TYPES:
            for schema_node in schema_nodes:
                for type_node in schema_node.findall(f"xmlns:{base_type}", self.xml_namespaces):
                    model.add_type(self.process_type_node(type_node, schema_node, base_type))

    @abstractmethod
    def process_operations(self, model: ODataModel) -> None:
        """Parses operations (functions/actions) and attaches them to their binding types."""

    def _attach_method(self, model: ODataModel, binding_type: str | None, method: MethodInformation) -> None:
        """Attaches an operation to its binding type, when that type is known."""
        if not binding_type:
            return
        type_schema = model.find_type(binding_type)
        if type_schema is not None:
            type_schema.add_method(method)

    @staticmethod
    def _new_navigation(node: Element) -> PropertyInformation:
        """Creates the common part of a navigation property schema."""
        schema = PropertyInformation()
        schema.Name = node.get("Name") or ""
        schema.IsNavigation = True
        return schema

    @staticmethod
    def parse_parameters(node: Element, namespaces: Dict[str, str]) -> list:
        """Extracts ``<Parameter>`` children into plain dicts."""
        return [
            {
                "Name": param.get("Name"),
                "Type": param.get("Type"),
                "Nullable": param.get("Nullable") != "false",
            }
            for param in node.findall("xmlns:Parameter", namespaces)
        ]

    def process_type_node(self, type_node: Element, schema_node: Element, base_type: str) -> TypeInformation:
        type_schema = TypeInformation()
        type_name = type_node.get("Name")
        if type_name is None:
            raise ValueError("Type node missing 'Name' attribute")
        type_schema.FullName = f"{schema_node.attrib['Namespace']}.{ODataType.normalize_class_name(type_name)}"
        type_schema.BaseTypeFullName = base_type
        type_schema.IsValueObject = base_type == "EntityType"

        if base_type == "EnumType":
            for member_node in type_node.findall("xmlns:Member", self.xml_namespaces):
                type_schema.add_member(self.process_member_node(member_node))
        else:
            for prop_node in type_node.findall("xmlns:Property", self.xml_namespaces):
                type_schema.add_property(self.process_property_node(prop_node))

            for prop_node in type_node.findall("xmlns:NavigationProperty", self.xml_namespaces):
                schema = self.process_navigation_property_node(prop_node)
                if schema:
                    type_schema.add_property(schema)

        return type_schema

    @abstractmethod
    def process_navigation_property_node(self, node: Element) -> Optional[PropertyInformation]:
        pass

    def process_property_node(self, node: Element) -> PropertyInformation:
        schema = PropertyInformation()
        schema.Name = node.get("Name") or ""
        schema.TypeName = node.get("Type")
        return schema

    def process_member_node(self, node: Element) -> MemberInformation:
        schema = MemberInformation()
        schema.Name = node.get("Name") or ""
        schema.Value = node.get("Value")
        return schema
