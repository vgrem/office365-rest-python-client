from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class UserMoveJobEntityData(Entity):
    @odata(name="HasOdbInSourceDataLocation")
    @property
    def has_odb_in_source_data_location(self) -> Optional[bool]:
        """Gets the HasOdbInSourceDataLocation property"""
        return self.properties.get("HasOdbInSourceDataLocation", None)

    @odata(name="UserPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the UserPrincipalName property"""
        return self.properties.get("UserPrincipalName", None)

    @odata(name="ValidationResult")
    @property
    def validation_result(self) -> Optional[int]:
        """Gets the ValidationResult property"""
        return self.properties.get("ValidationResult", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.UserMoveJobEntityData"
