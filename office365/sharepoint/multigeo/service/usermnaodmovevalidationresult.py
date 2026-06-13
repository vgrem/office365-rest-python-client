from typing import Optional

from office365.sharepoint.entity import Entity


class UserMnAODMoveValidationResult(Entity):
    @property
    def result(self) -> Optional[str]:
        """Gets the Result property"""
        return self.properties.get("Result", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.UserMnAODMoveValidationResult"
