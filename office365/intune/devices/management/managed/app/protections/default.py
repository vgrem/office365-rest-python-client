from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.managed.app.dataencryptiontype import (
    ManagedAppDataEncryptionType,
)
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.key_value_pair import KeyValuePair
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.managed.app_policy_deployment_summary import (
        ManagedAppPolicyDeploymentSummary,
    )
    from office365.intune.devices.management.managed.mobile_app import ManagedMobileApp


class DefaultManagedAppProtection(Entity):
    @odata(name="appDataEncryptionType")
    @property
    def app_data_encryption_type(self) -> ManagedAppDataEncryptionType:
        """Gets the appDataEncryptionType property"""
        return self.properties.get("appDataEncryptionType", ManagedAppDataEncryptionType.useDeviceSettings)

    @odata(name="customSettings")
    @property
    def custom_settings(self) -> ClientValueCollection[KeyValuePair]:
        """Gets the customSettings property"""
        return self.properties.get("customSettings", ClientValueCollection[KeyValuePair](KeyValuePair))

    @odata(name="deployedAppCount")
    @property
    def deployed_app_count(self) -> Optional[int]:
        """Gets the deployedAppCount property"""
        return self.properties.get("deployedAppCount", None)

    @odata(name="disableAppEncryptionIfDeviceEncryptionIsEnabled")
    @property
    def disable_app_encryption_if_device_encryption_is_enabled(self) -> Optional[bool]:
        """Gets the disableAppEncryptionIfDeviceEncryptionIsEnabled property"""
        return self.properties.get("disableAppEncryptionIfDeviceEncryptionIsEnabled", None)

    @odata(name="encryptAppData")
    @property
    def encrypt_app_data(self) -> Optional[bool]:
        """Gets the encryptAppData property"""
        return self.properties.get("encryptAppData", None)

    @odata(name="faceIdBlocked")
    @property
    def face_id_blocked(self) -> Optional[bool]:
        """Gets the faceIdBlocked property"""
        return self.properties.get("faceIdBlocked", None)

    @odata(name="minimumRequiredPatchVersion")
    @property
    def minimum_required_patch_version(self) -> Optional[str]:
        """Gets the minimumRequiredPatchVersion property"""
        return self.properties.get("minimumRequiredPatchVersion", None)

    @odata(name="minimumRequiredSdkVersion")
    @property
    def minimum_required_sdk_version(self) -> Optional[str]:
        """Gets the minimumRequiredSdkVersion property"""
        return self.properties.get("minimumRequiredSdkVersion", None)

    @odata(name="minimumWarningPatchVersion")
    @property
    def minimum_warning_patch_version(self) -> Optional[str]:
        """Gets the minimumWarningPatchVersion property"""
        return self.properties.get("minimumWarningPatchVersion", None)

    @odata(name="screenCaptureBlocked")
    @property
    def screen_capture_blocked(self) -> Optional[bool]:
        """Gets the screenCaptureBlocked property"""
        return self.properties.get("screenCaptureBlocked", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DefaultManagedAppProtection"

    @odata(name="apps", navigation=True)
    @property
    def apps(self) -> EntityCollection[ManagedMobileApp]:
        """Gets the apps property"""
        from office365.intune.devices.management.managed.mobile_app import ManagedMobileApp

        return self.properties.get(
            "apps",
            EntityCollection[ManagedMobileApp](self.context, ManagedMobileApp, ResourcePath("apps", self.resource_path)),
        )

    @odata(name="deploymentSummary", navigation=True)
    @property
    def deployment_summary(self) -> ManagedAppPolicyDeploymentSummary:
        """Gets the deploymentSummary property"""
        from office365.intune.devices.management.managed.app_policy_deployment_summary import (
            ManagedAppPolicyDeploymentSummary,
        )

        return self.properties.get(
            "deploymentSummary",
            ManagedAppPolicyDeploymentSummary(self.context, ResourcePath("deploymentSummary", self.resource_path)),
        )
