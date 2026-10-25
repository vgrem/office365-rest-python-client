from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ComponentContextInfo(Entity):
    """This class functions as a wrapper of the ContextInfo object. Reserved for internal use only."""

    @odata(name="SerializedData")
    @property
    def serialized_data(self) -> Optional[str]:
        """"""
        return self.properties.get("SerializedData", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.ClientSideComponent.ComponentContextInfo"
