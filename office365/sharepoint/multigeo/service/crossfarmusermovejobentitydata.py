from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class CrossFarmUserMoveJobEntityData(Entity):
    @odata(name="TextPayload")
    @property
    def text_payload(self) -> Optional[str]:
        """Gets the TextPayload property"""
        return self.properties.get("TextPayload", None)

    @odata(name="WorkflowData")
    @property
    def workflow_data(self) -> Optional[str]:
        """Gets the WorkflowData property"""
        return self.properties.get("WorkflowData", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossFarmUserMoveJobEntityData"
