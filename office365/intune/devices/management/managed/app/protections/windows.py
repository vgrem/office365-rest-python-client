from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.managed.app.protections.targeted_managed_app_policy_assignment import (
        TargetedManagedAppPolicyAssignment,
    )
    from office365.intune.devices.management.managed.windows.information_protection_enforcement_level import (
        WindowsInformationProtectionEnforcementLevel,
    )
    from office365.intune.devices.management.windows_information_protection_app import (
        WindowsInformationProtectionApp,
    )
    from office365.intune.devices.management.windows_information_protection_app_locker_file import (
        WindowsInformationProtectionAppLockerFile,
    )
    from office365.intune.devices.management.windows_information_protection_data_recovery_certificate import (
        WindowsInformationProtectionDataRecoveryCertificate,
    )
    from office365.intune.devices.management.windows_information_protection_ip_range_collection import (
        WindowsInformationProtectionIPRangeCollection,
    )
    from office365.intune.devices.management.windows_information_protection_proxied_domain_collection import (
        WindowsInformationProtectionProxiedDomainCollection,
    )
    from office365.intune.devices.management.windows_information_protection_resource_collection import (
        WindowsInformationProtectionResourceCollection,
    )


class WindowsInformationProtection(Entity):
    @odata(name="azureRightsManagementServicesAllowed")
    @property
    def azure_rights_management_services_allowed(self) -> Optional[bool]:
        """Gets the azureRightsManagementServicesAllowed property"""
        return self.properties.get("azureRightsManagementServicesAllowed", None)

    @odata(name="enterpriseDomain")
    @property
    def enterprise_domain(self) -> Optional[str]:
        """Gets the enterpriseDomain property"""
        return self.properties.get("enterpriseDomain", None)

    @odata(name="enterpriseIPRangesAreAuthoritative")
    @property
    def enterprise_ip_ranges_are_authoritative(self) -> Optional[bool]:
        """Gets the enterpriseIPRangesAreAuthoritative property"""
        return self.properties.get("enterpriseIPRangesAreAuthoritative", None)

    @odata(name="enterpriseProxyServersAreAuthoritative")
    @property
    def enterprise_proxy_servers_are_authoritative(self) -> Optional[bool]:
        """Gets the enterpriseProxyServersAreAuthoritative property"""
        return self.properties.get("enterpriseProxyServersAreAuthoritative", None)

    @odata(name="iconsVisible")
    @property
    def icons_visible(self) -> Optional[bool]:
        """Gets the iconsVisible property"""
        return self.properties.get("iconsVisible", None)

    @odata(name="indexingEncryptedStoresOrItemsBlocked")
    @property
    def indexing_encrypted_stores_or_items_blocked(self) -> Optional[bool]:
        """Gets the indexingEncryptedStoresOrItemsBlocked property"""
        return self.properties.get("indexingEncryptedStoresOrItemsBlocked", None)

    @odata(name="isAssigned")
    @property
    def is_assigned(self) -> Optional[bool]:
        """Gets the isAssigned property"""
        return self.properties.get("isAssigned", None)

    @odata(name="protectionUnderLockConfigRequired")
    @property
    def protection_under_lock_config_required(self) -> Optional[bool]:
        """Gets the protectionUnderLockConfigRequired property"""
        return self.properties.get("protectionUnderLockConfigRequired", None)

    @odata(name="revokeOnUnenrollDisabled")
    @property
    def revoke_on_unenroll_disabled(self) -> Optional[bool]:
        """Gets the revokeOnUnenrollDisabled property"""
        return self.properties.get("revokeOnUnenrollDisabled", None)

    @odata(name="rightsManagementServicesTemplateId")
    @property
    def rights_management_services_template_id(self) -> Optional[UUID]:
        """Gets the rightsManagementServicesTemplateId property"""
        return self.properties.get("rightsManagementServicesTemplateId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtection"

    @odata(name="dataRecoveryCertificate")
    @property
    def data_recovery_certificate(self) -> WindowsInformationProtectionDataRecoveryCertificate:
        """Gets the dataRecoveryCertificate property"""
        from office365.intune.devices.management.windows_information_protection_data_recovery_certificate import (
            WindowsInformationProtectionDataRecoveryCertificate,
        )

        return self.properties.get("dataRecoveryCertificate", WindowsInformationProtectionDataRecoveryCertificate())

    @odata(name="enforcementLevel")
    @property
    def enforcement_level(self) -> WindowsInformationProtectionEnforcementLevel:
        """Gets the enforcementLevel property"""
        from office365.intune.devices.management.managed.windows.information_protection_enforcement_level import (
            WindowsInformationProtectionEnforcementLevel,
        )

        return self.properties.get("enforcementLevel", WindowsInformationProtectionEnforcementLevel.noProtection)

    @odata(name="enterpriseInternalProxyServers")
    @property
    def enterprise_internal_proxy_servers(self) -> ClientValueCollection[WindowsInformationProtectionResourceCollection]:
        """Gets the enterpriseInternalProxyServers property"""
        from office365.intune.devices.management.windows_information_protection_resource_collection import (
            WindowsInformationProtectionResourceCollection,
        )

        return self.properties.get(
            "enterpriseInternalProxyServers",
            ClientValueCollection[WindowsInformationProtectionResourceCollection](
                WindowsInformationProtectionResourceCollection
            ),
        )

    @odata(name="enterpriseIPRanges")
    @property
    def enterprise_ip_ranges(self) -> ClientValueCollection[WindowsInformationProtectionIPRangeCollection]:
        """Gets the enterpriseIPRanges property"""
        from office365.intune.devices.management.windows_information_protection_ip_range_collection import (
            WindowsInformationProtectionIPRangeCollection,
        )

        return self.properties.get(
            "enterpriseIPRanges",
            ClientValueCollection[WindowsInformationProtectionIPRangeCollection](
                WindowsInformationProtectionIPRangeCollection
            ),
        )

    @odata(name="enterpriseNetworkDomainNames")
    @property
    def enterprise_network_domain_names(self) -> ClientValueCollection[WindowsInformationProtectionResourceCollection]:
        """Gets the enterpriseNetworkDomainNames property"""
        from office365.intune.devices.management.windows_information_protection_resource_collection import (
            WindowsInformationProtectionResourceCollection,
        )

        return self.properties.get(
            "enterpriseNetworkDomainNames",
            ClientValueCollection[WindowsInformationProtectionResourceCollection](
                WindowsInformationProtectionResourceCollection
            ),
        )

    @odata(name="enterpriseProtectedDomainNames")
    @property
    def enterprise_protected_domain_names(self) -> ClientValueCollection[WindowsInformationProtectionResourceCollection]:
        """Gets the enterpriseProtectedDomainNames property"""
        from office365.intune.devices.management.windows_information_protection_resource_collection import (
            WindowsInformationProtectionResourceCollection,
        )

        return self.properties.get(
            "enterpriseProtectedDomainNames",
            ClientValueCollection[WindowsInformationProtectionResourceCollection](
                WindowsInformationProtectionResourceCollection
            ),
        )

    @odata(name="enterpriseProxiedDomains")
    @property
    def enterprise_proxied_domains(self) -> ClientValueCollection[WindowsInformationProtectionProxiedDomainCollection]:
        """Gets the enterpriseProxiedDomains property"""
        from office365.intune.devices.management.windows_information_protection_proxied_domain_collection import (
            WindowsInformationProtectionProxiedDomainCollection,
        )

        return self.properties.get(
            "enterpriseProxiedDomains",
            ClientValueCollection[WindowsInformationProtectionProxiedDomainCollection](
                WindowsInformationProtectionProxiedDomainCollection
            ),
        )

    @odata(name="enterpriseProxyServers")
    @property
    def enterprise_proxy_servers(self) -> ClientValueCollection[WindowsInformationProtectionResourceCollection]:
        """Gets the enterpriseProxyServers property"""
        from office365.intune.devices.management.windows_information_protection_resource_collection import (
            WindowsInformationProtectionResourceCollection,
        )

        return self.properties.get(
            "enterpriseProxyServers",
            ClientValueCollection[WindowsInformationProtectionResourceCollection](
                WindowsInformationProtectionResourceCollection
            ),
        )

    @odata(name="exemptApps")
    @property
    def exempt_apps(self) -> ClientValueCollection[WindowsInformationProtectionApp]:
        """Gets the exemptApps property"""
        from office365.intune.devices.management.windows_information_protection_app import (
            WindowsInformationProtectionApp,
        )

        return self.properties.get(
            "exemptApps", ClientValueCollection[WindowsInformationProtectionApp](WindowsInformationProtectionApp)
        )

    @odata(name="neutralDomainResources")
    @property
    def neutral_domain_resources(self) -> ClientValueCollection[WindowsInformationProtectionResourceCollection]:
        """Gets the neutralDomainResources property"""
        from office365.intune.devices.management.windows_information_protection_resource_collection import (
            WindowsInformationProtectionResourceCollection,
        )

        return self.properties.get(
            "neutralDomainResources",
            ClientValueCollection[WindowsInformationProtectionResourceCollection](
                WindowsInformationProtectionResourceCollection
            ),
        )

    @odata(name="protectedApps")
    @property
    def protected_apps(self) -> ClientValueCollection[WindowsInformationProtectionApp]:
        """Gets the protectedApps property"""
        from office365.intune.devices.management.windows_information_protection_app import (
            WindowsInformationProtectionApp,
        )

        return self.properties.get(
            "protectedApps", ClientValueCollection[WindowsInformationProtectionApp](WindowsInformationProtectionApp)
        )

    @odata(name="smbAutoEncryptedFileExtensions")
    @property
    def smb_auto_encrypted_file_extensions(
        self,
    ) -> ClientValueCollection[WindowsInformationProtectionResourceCollection]:
        """Gets the smbAutoEncryptedFileExtensions property"""
        from office365.intune.devices.management.windows_information_protection_resource_collection import (
            WindowsInformationProtectionResourceCollection,
        )

        return self.properties.get(
            "smbAutoEncryptedFileExtensions",
            ClientValueCollection[WindowsInformationProtectionResourceCollection](
                WindowsInformationProtectionResourceCollection
            ),
        )

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[TargetedManagedAppPolicyAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.management.managed.app.protections.targeted_managed_app_policy_assignment import (
            TargetedManagedAppPolicyAssignment,
        )

        return self.properties.get(
            "assignments",
            EntityCollection[TargetedManagedAppPolicyAssignment](
                self.context, TargetedManagedAppPolicyAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @odata(name="exemptAppLockerFiles", navigation=True)
    @property
    def exempt_app_locker_files(self) -> EntityCollection[WindowsInformationProtectionAppLockerFile]:
        """Gets the exemptAppLockerFiles property"""
        from office365.intune.devices.management.windows_information_protection_app_locker_file import (
            WindowsInformationProtectionAppLockerFile,
        )

        return self.properties.get(
            "exemptAppLockerFiles",
            EntityCollection[WindowsInformationProtectionAppLockerFile](
                self.context,
                WindowsInformationProtectionAppLockerFile,
                ResourcePath("exemptAppLockerFiles", self.resource_path),
            ),
        )

    @odata(name="protectedAppLockerFiles", navigation=True)
    @property
    def protected_app_locker_files(self) -> EntityCollection[WindowsInformationProtectionAppLockerFile]:
        """Gets the protectedAppLockerFiles property"""
        from office365.intune.devices.management.windows_information_protection_app_locker_file import (
            WindowsInformationProtectionAppLockerFile,
        )

        return self.properties.get(
            "protectedAppLockerFiles",
            EntityCollection[WindowsInformationProtectionAppLockerFile](
                self.context,
                WindowsInformationProtectionAppLockerFile,
                ResourcePath("protectedAppLockerFiles", self.resource_path),
            ),
        )
