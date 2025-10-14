from typing import Optional

from office365.sharepoint.entity import Entity


class RestoreWorkflowCount(Entity):

    @property
    def count(self) -> Optional[int]:
        """Gets the Count property"""
        return self.properties.get("Count", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.RestoreWorkflowCount"
