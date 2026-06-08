from typing import List, Optional

from office365.admin.sharepoint.idle_session_signout import IdleSessionSignOut
from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class SharepointSettings(Entity):
    """Represents the tenant-level settings for SharePoint and OneDrive."""

    @odata(name="allowedDomainGuidsForSyncApp")
    @property
    def allowed_domain_guids_for_sync_app(self) -> StringCollection:
        """Collection of trusted domain GUIDs for the OneDrive sync app."""
        return self.properties.get("allowedDomainGuidsForSyncApp", StringCollection())

    @odata(name="availableManagedPathsForSiteCreation")
    @property
    def available_managed_paths_for_site_creation(self) -> StringCollection:
        """Collection of managed paths available for site creation."""
        return self.properties.get("availableManagedPathsForSiteCreation", StringCollection())

    @odata(name="excludedFileExtensionsForSyncApp")
    @property
    def excluded_file_extensions_for_sync_app(self) -> StringCollection:
        """Collection of file extensions not uploaded by the OneDrive sync app."""
        return self.properties.get("excludedFileExtensionsForSyncApp", StringCollection())

    @odata(name="idleSessionSignOut")
    @property
    def idle_session_sign_out(self) -> IdleSessionSignOut:
        """Specifies the idle session sign-out policies for the tenant."""
        return self.properties.get("idleSessionSignOut", IdleSessionSignOut())

    @property
    def is_commenting_on_site_pages_enabled(self) -> Optional[bool]:
        """Indicates whether comments are allowed on modern site pages in SharePoint."""
        return self.properties.get("isCommentingOnSitePagesEnabled", None)

    @property
    def is_legacy_auth_protocols_enabled(self) -> Optional[bool]:
        """Indicates whether legacy authentication protocols are enabled for the tenant."""
        return self.properties.get("isLegacyAuthProtocolsEnabled", None)

    @odata(name="sharingAllowedDomainList")
    @property
    def sharing_allowed_domain_list(self) -> StringCollection:
        """
        Collection of email domains that are allowed for sharing outside the organization.
        """
        return self.properties.get("sharingAllowedDomainList", StringCollection())

    @odata(name="sharingBlockedDomainList")
    @property
    def sharing_blocked_domain_list(self) -> StringCollection:
        """
        Collection of email domains that are blocked for sharing outside the organization.
        """
        return self.properties.get("sharingBlockedDomainList", StringCollection())

    @sharing_blocked_domain_list.setter
    def sharing_blocked_domain_list(self, value: List[str]) -> None:
        """Sets the collection of email domains that are blocked for sharing outside the organization."""
        self.set_property("sharingBlockedDomainList", value)

    @property
    def sharing_capability(self) -> Optional[str]:
        """
        Sharing capability for the tenant.
        Possible values are:
            disabled,
            externalUserSharingOnly,
            externalUserAndGuestSharing,
            existingExternalUserSharingOnly.
        """
        return self.properties.get("sharingCapability", None)

    @property
    def sharing_domain_restriction_mode(self) -> Optional[str]:
        """
        Specifies the external sharing mode for domains. Possible values are: none, allowList, blockList.
        """
        return self.properties.get("sharingDomainRestrictionMode", None)

    @property
    def site_creation_default_managed_path(self) -> Optional[str]:
        """
        The value of the team site managed path. This is the path under which new team sites will be created.
        """
        return self.properties.get("siteCreationDefaultManagedPath", None)

    @property
    def site_creation_default_storage_limit_in_mb(self) -> Optional[int]:
        """The default storage quota for a new site upon creation. Measured in megabytes (MB)."""
        return self.properties.get("siteCreationDefaultStorageLimitInMB", None)

    @property
    def tenant_default_timezone(self) -> Optional[str]:
        """
        The default timezone of a tenant for newly created sites. For a list of possible values,
        see SPRegionalSettings.TimeZones property.
        """
        return self.properties.get("tenantDefaultTimezone", None)

    @property
    def entity_type_name(self) -> str:
        return None  # type: ignore
