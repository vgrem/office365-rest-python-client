from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class RemovedStatus(Entity):
    @odata(name="ErrorCode")
    @property
    def error_code(self) -> Optional[int]:
        """Gets the ErrorCode property"""
        return self.properties.get("ErrorCode", None)

    @odata(name="FoundAndRemovedFile")
    @property
    def found_and_removed_file(self) -> Optional[bool]:
        """Gets the FoundAndRemovedFile property"""
        return self.properties.get("FoundAndRemovedFile", None)

    @odata(name="Succeeded")
    @property
    def succeeded(self) -> Optional[bool]:
        """Gets the Succeeded property"""
        return self.properties.get("Succeeded", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.FilePublish.Model.RemovedStatus"
