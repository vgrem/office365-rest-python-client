from typing import Dict, Optional
from xml.etree.ElementTree import Element

from office365.runtime.odata.property import PropertyInformation
from office365.runtime.odata.reader import ODataReader


class ODataV4Reader(ODataReader):
    """OData v4 reader"""

    def process_navigation_property_node(self, node: Element) -> Optional[PropertyInformation]:
        schema = PropertyInformation()
        schema.Name = node.get("Name")
        schema.TypeName = node.get("Type")
        schema.IsNavigation = True
        schema.IsBeta = False

        return schema

    @property
    def xml_namespaces(self) -> Dict[str, str]:
        return {
            "xmlns": "http://docs.oasis-open.org/odata/ns/edm",
            "edmx": "http://docs.oasis-open.org/odata/ns/edmx",
        }
