from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ApprovalRequestSyncResponse(Entity):
    @odata(name="ApprovalRequest")
    @property
    def approval_request(self) -> Optional[str]:
        """Gets the ApprovalRequest property"""
        return self.properties.get("ApprovalRequest", None)

    @odata(name="PublicationStatus")
    @property
    def publication_status(self) -> Optional[int]:
        """Gets the PublicationStatus property"""
        return self.properties.get("PublicationStatus", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.ApprovalRequestSyncResponse"
