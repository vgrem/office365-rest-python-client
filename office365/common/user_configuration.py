from __future__ import annotations

from typing import Optional

from office365.common.structured_data_entry import StructuredDataEntry
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserConfiguration(Entity):
    @odata(name="binaryData")
    @property
    def binary_data(self) -> Optional[bytes]:
        """Gets the binaryData property"""
        return self.properties.get("binaryData", None)

    @odata(name="structuredData")
    @property
    def structured_data(self) -> ClientValueCollection[StructuredDataEntry]:
        """Gets the structuredData property"""
        return self.properties.get("structuredData", ClientValueCollection[StructuredDataEntry](StructuredDataEntry))

    @odata(name="xmlData")
    @property
    def xml_data(self) -> Optional[bytes]:
        """Gets the xmlData property"""
        return self.properties.get("xmlData", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserConfiguration"
