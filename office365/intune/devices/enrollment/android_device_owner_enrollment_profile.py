from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.common.mime_content import MimeContent
from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class AndroidDeviceOwnerEnrollmentProfile(Entity):
    @odata(name="accountId")
    @property
    def account_id(self) -> Optional[str]:
        """Gets the accountId property"""
        return self.properties.get("accountId", None)

    @odata(name="configureWifi")
    @property
    def configure_wifi(self) -> Optional[bool]:
        """Gets the configureWifi property"""
        return self.properties.get("configureWifi", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="deviceNameTemplate")
    @property
    def device_name_template(self) -> Optional[str]:
        """Gets the deviceNameTemplate property"""
        return self.properties.get("deviceNameTemplate", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="enrolledDeviceCount")
    @property
    def enrolled_device_count(self) -> Optional[int]:
        """Gets the enrolledDeviceCount property"""
        return self.properties.get("enrolledDeviceCount", None)

    @odata(name="enrollmentTokenUsageCount")
    @property
    def enrollment_token_usage_count(self) -> Optional[int]:
        """Gets the enrollmentTokenUsageCount property"""
        return self.properties.get("enrollmentTokenUsageCount", None)

    @odata(name="isTeamsDeviceProfile")
    @property
    def is_teams_device_profile(self) -> Optional[bool]:
        """Gets the isTeamsDeviceProfile property"""
        return self.properties.get("isTeamsDeviceProfile", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="qrCodeContent")
    @property
    def qr_code_content(self) -> Optional[str]:
        """Gets the qrCodeContent property"""
        return self.properties.get("qrCodeContent", None)

    @odata(name="qrCodeImage")
    @property
    def qr_code_image(self) -> MimeContent:
        """Gets the qrCodeImage property"""
        return self.properties.get("qrCodeImage", MimeContent())

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="tokenCreationDateTime")
    @property
    def token_creation_date_time(self) -> Optional[datetime]:
        """Gets the tokenCreationDateTime property"""
        return self.properties.get("tokenCreationDateTime", None)

    @odata(name="tokenExpirationDateTime")
    @property
    def token_expiration_date_time(self) -> Optional[datetime]:
        """Gets the tokenExpirationDateTime property"""
        return self.properties.get("tokenExpirationDateTime", None)

    @odata(name="tokenValue")
    @property
    def token_value(self) -> Optional[str]:
        """Gets the tokenValue property"""
        return self.properties.get("tokenValue", None)

    @odata(name="wifiHidden")
    @property
    def wifi_hidden(self) -> Optional[bool]:
        """Gets the wifiHidden property"""
        return self.properties.get("wifiHidden", None)

    @odata(name="wifiPassword")
    @property
    def wifi_password(self) -> Optional[str]:
        """Gets the wifiPassword property"""
        return self.properties.get("wifiPassword", None)

    @odata(name="wifiSsid")
    @property
    def wifi_ssid(self) -> Optional[str]:
        """Gets the wifiSsid property"""
        return self.properties.get("wifiSsid", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidDeviceOwnerEnrollmentProfile"

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
        ],
    )
    def clear_enrollment_time_device_membership_target(self) -> Self:
        """clearEnrollmentTimeDeviceMembershipTarget operation."""
        qry = ServiceOperationQuery(self, "clearEnrollmentTimeDeviceMembershipTarget", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def create_token(self, token_validity_in_seconds: int) -> Self:
        """createToken operation.

        Args:
            token_validity_in_seconds (int):
                tokenValidityInSeconds parameter
        """
        qry = ServiceOperationQuery(
            self, "createToken", None, {"tokenValidityInSeconds": token_validity_in_seconds}, None, None
        )
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def revoke_token(self) -> Self:
        """revokeToken operation."""
        qry = ServiceOperationQuery(self, "revokeToken", None, {}, None, None)
        self.context.add_query(qry)
        return self
