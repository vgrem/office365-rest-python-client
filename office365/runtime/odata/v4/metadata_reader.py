from typing import Dict, Optional
from xml.etree.ElementTree import Element

from office365.runtime.odata.method import MethodInformation
from office365.runtime.odata.model import ODataModel
from office365.runtime.odata.property import PropertyInformation
from office365.runtime.odata.reader import ODataReader
from office365.runtime.odata.type import ODataType


class ODataV4Reader(ODataReader):
    """OData v4 reader"""

    def process_navigation_property_node(self, node: Element) -> Optional[PropertyInformation]:
        schema = PropertyInformation()
        schema.Name = node.get("Name") or ""
        schema.TypeName = node.get("Type")
        schema.IsNavigation = True
        schema.IsBeta = False

        return schema

    def process_method_node(self):
        pass

    def process_operations(self, model: ODataModel) -> None:
        assert self._root is not None
        nodes = self._root.findall(".//xmlns:Action", self.xml_namespaces)
        nodes += self._root.findall(".//xmlns:Function", self.xml_namespaces)
        for node in nodes:
            name = node.get("Name")
            params = self.parse_parameters(node, self.xml_namespaces)
            if not name or node.get("IsBound") != "true" or not params:
                continue  # unbound operations can't be attached to a generated type
            binding_param = params[0]
            if binding_param.get("Type") is None:
                continue
            binding_type = ODataType.normalize_type_name(binding_param["Type"])
            if binding_type is None:
                continue
            type_schema = model.types.get(binding_type)
            if type_schema is None:
                continue

            return_node = node.find("xmlns:ReturnType", self.xml_namespaces)
            return_type = return_node.get("Type") if return_node is not None else None
            kind = "action" if node.tag.endswith("Action") else "function"
            type_schema.add_method(
                MethodInformation(
                    Name=name,
                    Parameters=params[1:],
                    ReturnTypeFullName=return_type,
                    BindingTypeFullName=binding_type,
                    IsBound=True,
                    IsStatic=False,
                    Kind=kind,
                    IsSideEffecting=kind == "action",
                )
            )

    @property
    def xml_namespaces(self) -> Dict[str, str]:
        return {
            "xmlns": "http://docs.oasis-open.org/odata/ns/edm",
            "edmx": "http://docs.oasis-open.org/odata/ns/edmx",
        }
