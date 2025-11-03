from abc import ABC, abstractmethod
from typing import Dict, Optional
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from office365.runtime.odata.member import MemberInformation
from office365.runtime.odata.model import ODataModel
from office365.runtime.odata.property import PropertyInformation
from office365.runtime.odata.type_information import TypeInformation


def _normalize_class_name(name: str) -> str:
    return name[0].upper() + name[1:]


class ODataReader(ABC):
    """OData reader"""

    def __init__(self, metadata_path: str):
        self._metadata_path = metadata_path
        self._root: Optional[Element] = None

    @property
    @abstractmethod
    def xml_namespaces(self) -> Dict[str, str]:
        """XML namespaces for the specific OData version"""
        pass

    def format_file(self):
        import xml.dom.minidom

        with open(self._metadata_path, "r", encoding="utf8") as in_file:
            metadata_content = in_file.read()

        formatted_metadata_content = xml.dom.minidom.parseString(metadata_content).toprettyxml()

        with open(self._metadata_path, "w", encoding="utf8") as out_file:
            out_file.write(formatted_metadata_content)

    def process_schema_node(self, model: ODataModel) -> None:
        self._root = ET.parse(self._metadata_path).getroot()
        schema_nodes = self._root.findall("edmx:DataServices/xmlns:Schema", self.xml_namespaces)

        # base_types = ["EnumType", "ComplexType"]
        # base_types = ["ComplexType", "EntityType"]
        # base_types = ["EntityType"]
        # base_types = ["EnumType"]
        base_types = ["ComplexType"]

        for base_type in base_types:
            for schema_node in schema_nodes:
                for type_node in schema_node.findall(f"xmlns:{base_type}", self.xml_namespaces):
                    type_schema = self.process_type_node(type_node, schema_node, base_type)
                    model.add_type(type_schema)

    def process_type_node(self, type_node: Element, schema_node: Element, base_type: str) -> TypeInformation:
        type_schema = TypeInformation()
        type_schema.FullName = f"{schema_node.attrib['Namespace']}.{_normalize_class_name(type_node.get('Name'))}"
        type_schema.BaseTypeFullName = base_type
        type_schema.IsValueObject = base_type == "EntityType"

        if base_type == "EnumType":
            for member_node in type_node.findall("xmlns:Member", self.xml_namespaces):
                schema = self.process_member_node(member_node)
                type_schema.add_member(schema)
        else:
            for prop_node in type_node.findall("xmlns:Property", self.xml_namespaces):
                schema = self.process_property_node(prop_node)
                type_schema.add_property(schema)

            for prop_node in type_node.findall("xmlns:NavigationProperty", self.xml_namespaces):
                schema = self.process_navigation_property_node(prop_node)
                if schema:
                    type_schema.add_property(schema)

        return type_schema

    def process_method_node(self):
        pass

    @abstractmethod
    def process_navigation_property_node(self, node: Element) -> Optional[PropertyInformation]:
        pass

    def process_property_node(self, node: Element) -> PropertyInformation:
        schema = PropertyInformation()
        schema.Name = node.get("Name")
        schema.TypeName = node.get("Type")
        return schema

    def process_member_node(self, node: Element) -> MemberInformation:
        schema = MemberInformation()
        schema.Name = node.get("Name")
        schema.Value = node.get("Value")
        return schema

    def generate_model(self):
        model = ODataModel()
        self.process_schema_node(model)
        return model
