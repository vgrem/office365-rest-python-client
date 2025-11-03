from typing import Dict, Optional
from xml.etree.ElementTree import Element

from office365.runtime.odata.property import PropertyInformation
from office365.runtime.odata.reader import ODataReader


class ODataV3Reader(ODataReader):
    """OData v3 reader"""

    def process_navigation_property_node(self, node: Element) -> Optional[PropertyInformation]:
        schema = PropertyInformation()
        schema.Name = node.get("Name")
        schema.IsNavigation = True

        relationship = node.get("Relationship")
        to_role = node.get("ToRole")
        # from_role = node.get("FromRole")

        association_name = relationship.split(".")[-1] if "." in relationship else relationship

        association_node = self._root.find(f".//xmlns:Association[@Name='{association_name}']", self.xml_namespaces)
        if association_node is None:
            return None

        end_node = association_node.find(f".//xmlns:End[@Role='{to_role}']", self.xml_namespaces)
        if end_node is None:
            return None

        multiplicity = end_node.get("Multiplicity")

        if multiplicity == "*":
            schema.TypeName = f"Collection({end_node.get('Type')})"
        else:
            schema.TypeName = end_node.get("Type")

        return schema

    @property
    def xml_namespaces(self) -> Dict[str, str]:
        return {
            "xmlns": "http://schemas.microsoft.com/ado/2009/11/edm",
            "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
            "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
        }
