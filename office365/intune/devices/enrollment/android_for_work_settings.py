from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class AndroidForWorkSettings(Entity):
    @odata(name="deviceOwnerManagementEnabled")
    @property
    def device_owner_management_enabled(self) -> Optional[bool]:
        """Gets the deviceOwnerManagementEnabled property"""
        return self.properties.get("deviceOwnerManagementEnabled", None)

    @odata(name="lastAppSyncDateTime")
    @property
    def last_app_sync_date_time(self) -> Optional[datetime]:
        """Gets the lastAppSyncDateTime property"""
        return self.properties.get("lastAppSyncDateTime", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="ownerOrganizationName")
    @property
    def owner_organization_name(self) -> Optional[str]:
        """Gets the ownerOrganizationName property"""
        return self.properties.get("ownerOrganizationName", None)

    @odata(name="ownerUserPrincipalName")
    @property
    def owner_user_principal_name(self) -> Optional[str]:
        """Gets the ownerUserPrincipalName property"""
        return self.properties.get("ownerUserPrincipalName", None)

    @odata(name="targetGroupIds")
    @property
    def target_group_ids(self) -> StringCollection:
        """Gets the targetGroupIds property"""
        return self.properties.get("targetGroupIds", StringCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidForWorkSettings"

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def complete_signup(self, enterprise_token: str) -> Self:
        """completeSignup operation.

        Args:
            enterprise_token (str):
                enterpriseToken parameter
        """
        qry = ServiceOperationQuery(self, "completeSignup", None, {"enterpriseToken": enterprise_token}, None, None)
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
    def request_signup_url(self, host_name: str) -> ClientResult[str]:
        """requestSignupUrl operation.

        Args:
            host_name (str):
                hostName parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "requestSignupUrl", None, {"hostName": host_name}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def sync_apps(self) -> Self:
        """syncApps operation."""
        qry = ServiceOperationQuery(self, "syncApps", None, {}, None, None)
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
    def unbind(self) -> Self:
        """unbind operation."""
        qry = ServiceOperationQuery(self, "unbind", None, {}, None, None)
        self.context.add_query(qry)
        return self
