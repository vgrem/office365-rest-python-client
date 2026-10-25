from typing import Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SpotlightResult(Entity):
    @odata(name="Order")
    @property
    def order(self) -> ClientValueCollection[int]:
        """Gets the Order property"""
        return self.properties.get("Order", ClientValueCollection(int))

    @odata(name="ResultCode")
    @property
    def result_code(self) -> Optional[int]:
        """Gets the ResultCode property"""
        return self.properties.get("ResultCode", None)

    @property
    def entity_type_name(self):
        return "SP.Utilities.SpotlightResult"
