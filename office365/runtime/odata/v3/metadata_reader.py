from typing import Dict, Optional
from xml.etree.ElementTree import Element

from office365.runtime.odata.method import MethodInformation
from office365.runtime.odata.model import ODataModel
from office365.runtime.odata.property import PropertyInformation
from office365.runtime.odata.reader import ODataReader
from office365.runtime.odata.type import ODataType

_MIN_TYPE_ENCODED_PARTS = 3


class ODataV3Reader(ODataReader):
    """OData v3 reader"""

    def process_navigation_property_node(self, node: Element) -> Optional[PropertyInformation]:
        schema = PropertyInformation()
        schema.Name = node.get("Name") or ""
        schema.IsNavigation = True

        relationship = node.get("Relationship")
        if relationship is None:
            return None
        to_role = node.get("ToRole")
        if to_role is None:
            return None

        association_name = relationship.split(".")[-1] if "." in relationship else relationship

        assert self._root is not None
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

    def process_method_node(self):
        pass

    def process_operations(self, model: ODataModel) -> None:
        assert self._root is not None
        for node in self._root.findall(".//xmlns:FunctionImport", self.xml_namespaces):
            name = node.get("Name")
            if not name or node.get("EntitySet") is not None:
                continue  # entity-set accessor -> navigation property

            params = self.parse_parameters(node, self.xml_namespaces)
            is_bindable = node.get("IsBindable") == "true" or any(p.get("Name") == "this" for p in params)

            if is_bindable:
                binding_param = next((p for p in params if p.get("Name") == "this"), params[0] if params else None)
                if binding_param is None or binding_param.get("Type") is None:
                    continue
                binding_type = ODataType.normalize_type_name(binding_param["Type"])
                method_name = name
                remaining = [p for p in params if p is not binding_param]
                is_static = False
            else:
                parts = name.split("_")
                if len(parts) < _MIN_TYPE_ENCODED_PARTS or parts[0] != "SP":
                    continue  # unbound, not type-encoded -> cannot attach
                binding_type = f"SP.{parts[1]}"
                method_name = "".join(parts[2:])
                remaining = params
                is_static = True

            if binding_type is None:
                continue
            type_schema = model.types.get(binding_type)
            if type_schema is None:
                continue

            is_composable = node.get("IsComposable") == "true"
            is_side_effecting = node.get("IsSideEffecting") != "false"
            kind = "function" if (is_composable or not is_side_effecting) else "action"
            type_schema.add_method(
                MethodInformation(
                    Name=method_name,
                    Parameters=remaining,
                    ReturnTypeFullName=node.get("ReturnType"),
                    BindingTypeFullName=binding_type,
                    IsBound=is_bindable,
                    IsStatic=is_static,
                    Kind=kind,
                    IsComposable=is_composable,
                    IsSideEffecting=is_side_effecting,
                )
            )

    @property
    def xml_namespaces(self) -> Dict[str, str]:
        return {
            "xmlns": "http://schemas.microsoft.com/ado/2009/11/edm",
            "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
            "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
        }
