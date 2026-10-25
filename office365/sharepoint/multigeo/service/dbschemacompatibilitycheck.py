from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class DBSchemaCompatibilityCheck(Entity):
    @odata(name="CompatibilityResult")
    @property
    def compatibility_result(self) -> Optional[str]:
        """Gets the CompatibilityResult property"""
        return self.properties.get("CompatibilityResult", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.DBSchemaCompatibilityCheck"
