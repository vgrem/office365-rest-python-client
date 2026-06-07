from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.entity import Entity


class WindowsInformationProtection(Entity):
    @property
    def azure_rights_management_services_allowed(self) -> Optional[bool]:
        """Gets the azureRightsManagementServicesAllowed property"""
        return self.properties.get("azureRightsManagementServicesAllowed", None)

    @property
    def enterprise_domain(self) -> Optional[str]:
        """Gets the enterpriseDomain property"""
        return self.properties.get("enterpriseDomain", None)

    @property
    def enterprise_ip_ranges_are_authoritative(self) -> Optional[bool]:
        """Gets the enterpriseIPRangesAreAuthoritative property"""
        return self.properties.get("enterpriseIPRangesAreAuthoritative", None)

    @property
    def enterprise_proxy_servers_are_authoritative(self) -> Optional[bool]:
        """Gets the enterpriseProxyServersAreAuthoritative property"""
        return self.properties.get("enterpriseProxyServersAreAuthoritative", None)

    @property
    def icons_visible(self) -> Optional[bool]:
        """Gets the iconsVisible property"""
        return self.properties.get("iconsVisible", None)

    @property
    def indexing_encrypted_stores_or_items_blocked(self) -> Optional[bool]:
        """Gets the indexingEncryptedStoresOrItemsBlocked property"""
        return self.properties.get("indexingEncryptedStoresOrItemsBlocked", None)

    @property
    def is_assigned(self) -> Optional[bool]:
        """Gets the isAssigned property"""
        return self.properties.get("isAssigned", None)

    @property
    def protection_under_lock_config_required(self) -> Optional[bool]:
        """Gets the protectionUnderLockConfigRequired property"""
        return self.properties.get("protectionUnderLockConfigRequired", None)

    @property
    def revoke_on_unenroll_disabled(self) -> Optional[bool]:
        """Gets the revokeOnUnenrollDisabled property"""
        return self.properties.get("revokeOnUnenrollDisabled", None)

    @property
    def rights_management_services_template_id(self) -> Optional[UUID]:
        """Gets the rightsManagementServicesTemplateId property"""
        return self.properties.get("rightsManagementServicesTemplateId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtection"
