from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.intune.devices.management.virtualendpoint.cloudpcs.provisioningtype import CloudPcProvisioningType
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.intune.devices.cloud_pc_launch_detail import CloudPcLaunchDetail
    from office365.intune.devices.management.virtualendpoint.cloudpcs.cloud_pc_operating_system import (
        CloudPcOperatingSystem,
    )
    from office365.intune.devices.management.virtualendpoint.cloudpcs.cloud_pc_user_account_type import (
        CloudPcUserAccountType,
    )


class CloudPC(Entity):
    @odata(name="aadDeviceId")
    @property
    def aad_device_id(self) -> Optional[str]:
        """Gets the aadDeviceId property"""
        return self.properties.get("aadDeviceId", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="gracePeriodEndDateTime")
    @property
    def grace_period_end_date_time(self) -> datetime:
        """Gets the gracePeriodEndDateTime property"""
        return self.properties.get("gracePeriodEndDateTime", datetime.min)

    @odata(name="imageDisplayName")
    @property
    def image_display_name(self) -> Optional[str]:
        """Gets the imageDisplayName property"""
        return self.properties.get("imageDisplayName", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="managedDeviceId")
    @property
    def managed_device_id(self) -> Optional[str]:
        """Gets the managedDeviceId property"""
        return self.properties.get("managedDeviceId", None)

    @odata(name="managedDeviceName")
    @property
    def managed_device_name(self) -> Optional[str]:
        """Gets the managedDeviceName property"""
        return self.properties.get("managedDeviceName", None)

    @odata(name="onPremisesConnectionName")
    @property
    def on_premises_connection_name(self) -> Optional[str]:
        """Gets the onPremisesConnectionName property"""
        return self.properties.get("onPremisesConnectionName", None)

    @odata(name="provisioningPolicyId")
    @property
    def provisioning_policy_id(self) -> Optional[str]:
        """Gets the provisioningPolicyId property"""
        return self.properties.get("provisioningPolicyId", None)

    @odata(name="provisioningPolicyName")
    @property
    def provisioning_policy_name(self) -> Optional[str]:
        """Gets the provisioningPolicyName property"""
        return self.properties.get("provisioningPolicyName", None)

    @odata(name="provisioningType")
    @property
    def provisioning_type(self) -> CloudPcProvisioningType:
        """Gets the provisioningType property"""
        return self.properties.get("provisioningType", CloudPcProvisioningType.dedicated)

    @odata(name="servicePlanId")
    @property
    def service_plan_id(self) -> Optional[str]:
        """Gets the servicePlanId property"""
        return self.properties.get("servicePlanId", None)

    @odata(name="servicePlanName")
    @property
    def service_plan_name(self) -> Optional[str]:
        """Gets the servicePlanName property"""
        return self.properties.get("servicePlanName", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPC"

    @verb(role="action", effect="write")
    @require_permission(delegated=["CloudPC.ReadWrite.All"], application=["CloudPC.ReadWrite.All"])
    def end_grace_period(self) -> Self:
        """endGracePeriod operation."""
        qry = ServiceOperationQuery(self, "endGracePeriod", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["CloudPC.ReadWrite.All"], application=["CloudPC.ReadWrite.All"])
    def reboot(self) -> Self:
        """reboot operation."""
        qry = ServiceOperationQuery(self, "reboot", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["CloudPC.ReadWrite.All"], application=["CloudPC.ReadWrite.All"])
    def rename(self, display_name: str) -> Self:
        """rename operation.

        Args:
            display_name (str):
                displayName parameter
        """
        qry = ServiceOperationQuery(self, "rename", None, {"displayName": display_name}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["CloudPC.ReadWrite.All"], application=["CloudPC.ReadWrite.All"])
    def reprovision(self, user_account_type: CloudPcUserAccountType, os_version: CloudPcOperatingSystem) -> Self:
        """reprovision operation.

        Args:
            user_account_type (CloudPcUserAccountType):
                userAccountType parameter
            os_version (CloudPcOperatingSystem):
                osVersion parameter
        """
        qry = ServiceOperationQuery(
            self, "reprovision", None, {"userAccountType": user_account_type, "osVersion": os_version}, None, None
        )
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["CloudPC.ReadWrite.All"], application=["CloudPC.ReadWrite.All"])
    def resize(self, target_service_plan_id: str) -> Self:
        """resize operation.

        Args:
            target_service_plan_id (str):
                targetServicePlanId parameter
        """
        qry = ServiceOperationQuery(self, "resize", None, {"targetServicePlanId": target_service_plan_id}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["CloudPC.ReadWrite.All"], application=["CloudPC.ReadWrite.All"])
    def restore(self, cloud_pc_snapshot_id: str) -> Self:
        """restore operation.

        Args:
            cloud_pc_snapshot_id (str):
                cloudPcSnapshotId parameter
        """
        qry = ServiceOperationQuery(self, "restore", None, {"cloudPcSnapshotId": cloud_pc_snapshot_id}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["CloudPC.ReadWrite.All"], application=["CloudPC.ReadWrite.All"])
    def troubleshoot(self) -> Self:
        """troubleshoot operation."""
        qry = ServiceOperationQuery(self, "troubleshoot", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="read")
    @require_permission(delegated=["CloudPC.Read.All", "CloudPC.ReadWrite.All"])
    def retrieve_cloud_pc_launch_detail(self) -> ClientResult[CloudPcLaunchDetail]:
        """retrieveCloudPcLaunchDetail operation."""
        from office365.intune.devices.cloud_pc_launch_detail import CloudPcLaunchDetail

        return_type = ClientResult(self.context, CloudPcLaunchDetail())
        qry = FunctionQuery(self, "retrieveCloudPcLaunchDetail", None, return_type)
        self.context.add_query(qry)
        return return_type
