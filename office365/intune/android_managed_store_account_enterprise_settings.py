from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.intune.android_enrollment_company_code import AndroidEnrollmentCompanyCode
from office365.intune.android_managed_store_account_app_sync_status import AndroidManagedStoreAccountAppSyncStatus
from office365.intune.android_managed_store_account_bind_status import AndroidManagedStoreAccountBindStatus
from office365.intune.android_managed_store_account_enrollment_target import AndroidManagedStoreAccountEnrollmentTarget
from office365.intune.managed_google_play_enterprise_type import ManagedGooglePlayEnterpriseType
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class AndroidManagedStoreAccountEnterpriseSettings(Entity):
    @odata(name="androidDeviceOwnerFullyManagedEnrollmentEnabled")
    @property
    def android_device_owner_fully_managed_enrollment_enabled(self) -> Optional[bool]:
        """Gets the androidDeviceOwnerFullyManagedEnrollmentEnabled property"""
        return self.properties.get("androidDeviceOwnerFullyManagedEnrollmentEnabled", None)

    @odata(name="bindStatus")
    @property
    def bind_status(self) -> Optional[AndroidManagedStoreAccountBindStatus]:
        """Gets the bindStatus property"""
        return self.properties.get("bindStatus", None)

    @odata(name="companyCodes")
    @property
    def company_codes(self) -> ClientValueCollection[AndroidEnrollmentCompanyCode]:
        """Gets the companyCodes property"""
        return self.properties.get(
            "companyCodes", ClientValueCollection[AndroidEnrollmentCompanyCode](AndroidEnrollmentCompanyCode)
        )

    @odata(name="deviceOwnerManagementEnabled")
    @property
    def device_owner_management_enabled(self) -> Optional[bool]:
        """Gets the deviceOwnerManagementEnabled property"""
        return self.properties.get("deviceOwnerManagementEnabled", None)

    @odata(name="enrollmentTarget")
    @property
    def enrollment_target(self) -> Optional[AndroidManagedStoreAccountEnrollmentTarget]:
        """Gets the enrollmentTarget property"""
        return self.properties.get("enrollmentTarget", None)

    @odata(name="lastAppSyncDateTime")
    @property
    def last_app_sync_date_time(self) -> Optional[datetime]:
        """Gets the lastAppSyncDateTime property"""
        return self.properties.get("lastAppSyncDateTime", None)

    @odata(name="lastAppSyncStatus")
    @property
    def last_app_sync_status(self) -> Optional[AndroidManagedStoreAccountAppSyncStatus]:
        """Gets the lastAppSyncStatus property"""
        return self.properties.get("lastAppSyncStatus", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="managedGooglePlayEnterpriseType")
    @property
    def managed_google_play_enterprise_type(self) -> Optional[ManagedGooglePlayEnterpriseType]:
        """Gets the managedGooglePlayEnterpriseType property"""
        return self.properties.get("managedGooglePlayEnterpriseType", None)

    @odata(name="managedGooglePlayInitialScopeTagIds")
    @property
    def managed_google_play_initial_scope_tag_ids(self) -> StringCollection:
        """Gets the managedGooglePlayInitialScopeTagIds property"""
        return self.properties.get("managedGooglePlayInitialScopeTagIds", StringCollection())

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
        return "microsoft.graph.AndroidManagedStoreAccountEnterpriseSettings"

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def add_apps(self, product_ids: list[str]) -> Self:
        """addApps operation.

        Args:
            product_ids (list[str]):
                productIds parameter
        """
        qry = ServiceOperationQuery(self, "addApps", None, {"productIds": StringCollection(product_ids)}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def approve_apps(self, package_ids: list[str], approve_all_permissions: bool) -> Self:
        """approveApps operation.

        Args:
            package_ids (list[str]):
                packageIds parameter
            approve_all_permissions (bool):
                approveAllPermissions parameter
        """
        qry = ServiceOperationQuery(
            self,
            "approveApps",
            None,
            {"packageIds": StringCollection(package_ids), "approveAllPermissions": approve_all_permissions},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
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
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def create_google_play_web_token(self, parent_uri: str) -> ClientResult[str]:
        """createGooglePlayWebToken operation.

        Args:
            parent_uri (str):
                parentUri parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "createGooglePlayWebToken", None, {"parentUri": parent_uri}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def create_zero_touch_web_token(self, parent_uri: str) -> ClientResult[str]:
        """createZeroTouchWebToken operation.

        Args:
            parent_uri (str):
                parentUri parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "createZeroTouchWebToken", None, {"parentUri": parent_uri}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def request_enterprise_upgrade_url(self) -> ClientResult[str]:
        """requestEnterpriseUpgradeUrl operation."""
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "requestEnterpriseUpgradeUrl", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
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
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def set_android_device_owner_fully_managed_enrollment_state(self, enabled: bool) -> Self:
        """setAndroidDeviceOwnerFullyManagedEnrollmentState operation.

        Args:
            enabled (bool):
                enabled parameter
        """
        qry = ServiceOperationQuery(
            self, "setAndroidDeviceOwnerFullyManagedEnrollmentState", None, {"enabled": enabled}, None, None
        )
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def sync_apps(self) -> Self:
        """syncApps operation."""
        qry = ServiceOperationQuery(self, "syncApps", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def unbind(self) -> Self:
        """unbind operation."""
        qry = ServiceOperationQuery(self, "unbind", None, {}, None, None)
        self.context.add_query(qry)
        return self
