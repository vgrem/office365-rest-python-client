from abc import ABC, abstractmethod
from typing import Dict
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from office365.runtime.odata.model import ODataModel
from office365.runtime.odata.property import ODataProperty
from office365.runtime.odata.type import ODataType


class ODataReader(ABC):
    """OData reader"""

    def __init__(self, metadata_path: str):
        self._metadata_path = metadata_path

    @property
    @abstractmethod
    def xml_namespaces(self) -> Dict[str, str]:
        """XML namespaces for the specific OData version"""
        pass

    def format_file(self):
        import xml.dom.minidom

        with open(self._metadata_path, "r", encoding="utf8") as in_file:
            metadata_content = in_file.read()

        formatted_metadata_content = xml.dom.minidom.parseString(
            metadata_content
        ).toprettyxml()

        with open(self._metadata_path, "w", encoding="utf8") as out_file:
            out_file.write(formatted_metadata_content)

    def process_schema_node(self, model: ODataModel) -> None:
        root = ET.parse(self._metadata_path).getroot()
        schema_node = root.find("edmx:DataServices/xmlns:Schema", self.xml_namespaces)
        for type_node in schema_node.findall("xmlns:ComplexType", self.xml_namespaces):
            type_schema = self.process_type_node(type_node, schema_node)
            model.add_type(type_schema)

    def process_type_node(self, type_node: Element, schema_node: Element) -> ODataType:
        type_schema = ODataType()
        type_schema.namespace = schema_node.attrib["Namespace"]
        type_schema.className = type_node.get("Name")
        type_schema.baseType = "ComplexType"

        for prop_node in type_node.findall("xmlns:Property", self.xml_namespaces):
            prop_schema = self.process_property_node(prop_node)
            type_schema.add_property(prop_schema)

        return type_schema

    def process_method_node(self):
        pass

    def process_property_node(self, node: Element) -> ODataProperty:
        prop_schema = ODataProperty()
        prop_schema.name = node.get("Name")
        prop_schema.type_name = node.get("Type")
        return prop_schema

    def generate_model(self):
        model = ODataModel()
        self.process_schema_node(model)
        return model
