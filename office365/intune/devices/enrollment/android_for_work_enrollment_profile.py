from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.intune.mime_content import MimeContent
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version


@version("beta")
class AndroidForWorkEnrollmentProfile(Entity):
    @odata(name="accountId")
    @property
    def account_id(self) -> Optional[str]:
        """Gets the accountId property"""
        return self.properties.get("accountId", None)

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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidForWorkEnrollmentProfile"

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
