from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.reports.migrationstatus import MigrationStatus
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.key_value_pair import KeyValuePair


class RelyingPartyDetailedSummary(Entity):
    @property
    def failed_sign_in_count(self) -> Optional[int]:
        """Gets the failedSignInCount property"""
        return self.properties.get("failedSignInCount", None)

    @property
    def migration_status(self) -> MigrationStatus:
        """Gets the migrationStatus property"""
        return self.properties.get("migrationStatus", MigrationStatus.ready)

    @property
    def migration_validation_details(self) -> ClientValueCollection[KeyValuePair]:
        """Gets the migrationValidationDetails property"""
        return self.properties.get("migrationValidationDetails", ClientValueCollection[KeyValuePair](KeyValuePair))

    @property
    def relying_party_id(self) -> Optional[str]:
        """Gets the relyingPartyId property"""
        return self.properties.get("relyingPartyId", None)

    @property
    def relying_party_name(self) -> Optional[str]:
        """Gets the relyingPartyName property"""
        return self.properties.get("relyingPartyName", None)

    @property
    def reply_urls(self) -> StringCollection:
        """Gets the replyUrls property"""
        return self.properties.get("replyUrls", StringCollection(None))

    @property
    def service_id(self) -> Optional[str]:
        """Gets the serviceId property"""
        return self.properties.get("serviceId", None)

    @property
    def sign_in_success_rate(self) -> Optional[float]:
        """Gets the signInSuccessRate property"""
        return self.properties.get("signInSuccessRate", None)

    @property
    def successful_sign_in_count(self) -> Optional[int]:
        """Gets the successfulSignInCount property"""
        return self.properties.get("successfulSignInCount", None)

    @property
    def total_sign_in_count(self) -> Optional[int]:
        """Gets the totalSignInCount property"""
        return self.properties.get("totalSignInCount", None)

    @property
    def unique_user_count(self) -> Optional[int]:
        """Gets the uniqueUserCount property"""
        return self.properties.get("uniqueUserCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RelyingPartyDetailedSummary"
