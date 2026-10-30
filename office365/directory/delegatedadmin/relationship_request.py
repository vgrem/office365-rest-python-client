from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.delegatedadmin.relationshiprequestaction import DelegatedAdminRelationshipRequestAction
from office365.directory.delegatedadmin.relationshiprequeststatus import DelegatedAdminRelationshipRequestStatus
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class DelegatedAdminRelationshipRequest(Entity):
    @odata(name="action")
    @property
    def action(self) -> DelegatedAdminRelationshipRequestAction:
        """Gets the action property"""
        return self.properties.get("action", DelegatedAdminRelationshipRequestAction.lockForApproval)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> DelegatedAdminRelationshipRequestStatus:
        """Gets the status property"""
        return self.properties.get("status", DelegatedAdminRelationshipRequestStatus.created)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DelegatedAdminRelationshipRequest"
