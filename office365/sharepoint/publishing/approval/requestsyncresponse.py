from typing import Optional

from office365.sharepoint.entity import Entity


class ApprovalRequestSyncResponse(Entity):
    @property
    def approval_request(self) -> Optional[str]:
        """Gets the ApprovalRequest property"""
        return self.properties.get("ApprovalRequest", None)

    @property
    def publication_status(self) -> Optional[int]:
        """Gets the PublicationStatus property"""
        return self.properties.get("PublicationStatus", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.ApprovalRequestSyncResponse"
