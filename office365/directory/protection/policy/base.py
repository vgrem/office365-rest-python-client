from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.directory.permissions.identity_set import IdentitySet
from office365.directory.policies.protection_policy_artifact_count import ProtectionPolicyArtifactCount
from office365.directory.policies.retention_setting import RetentionSetting
from office365.directory.protection.policystatus import ProtectionPolicyStatus
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata


class ProtectionPolicyBase(Entity):
    """
    Contains details about protection policies applied to Microsoft 365 data in an organization.
    Protection policies are defined by the Global Admin (or the SharePoint Online Admin or Exchange Online Admin)
    and include what data to protect, when to protect it, and for what time period to retain the protected data
    for a single Microsoft 365 service.
    """

    def activate(self) -> Self:
        """Activate the protection policy so protection starts for its units."""
        qry = ServiceOperationQuery(self, "activate", return_type=self)
        self.context.add_query(qry)
        return self

    def deactivate(self) -> Self:
        """Deactivate the protection policy (protection stops for its units)."""
        qry = ServiceOperationQuery(self, "deactivate", return_type=self)
        self.context.add_query(qry)
        return self

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Identity of the user, device, or application which created the item."""
        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="protectionPolicyArtifactCount")
    @property
    def protection_policy_artifact_count(self) -> ProtectionPolicyArtifactCount:
        """Gets the protectionPolicyArtifactCount property"""
        return self.properties.get("protectionPolicyArtifactCount", ProtectionPolicyArtifactCount())

    @odata(name="retentionSettings")
    @property
    def retention_settings(self) -> ClientValueCollection[RetentionSetting]:
        """Gets the retentionSettings property"""
        return self.properties.get("retentionSettings", ClientValueCollection[RetentionSetting](RetentionSetting))

    @odata(name="status")
    @property
    def status(self) -> ProtectionPolicyStatus:
        """Gets the status property"""
        return self.properties.get("status", ProtectionPolicyStatus.inactive)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProtectionPolicyBase"
