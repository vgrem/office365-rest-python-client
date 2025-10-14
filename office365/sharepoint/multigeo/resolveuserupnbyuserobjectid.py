from typing import Optional

from office365.sharepoint.entity import Entity


class ResolveUserUpnByUserObjectId(Entity):

    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the UserPrincipalName property"""
        return self.properties.get("UserPrincipalName", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.ResolveUserUpnByUserObjectId"
