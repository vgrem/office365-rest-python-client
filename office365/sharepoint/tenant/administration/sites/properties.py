from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.onedrive.listitems.list_item import ListItem
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.paths.v3.entity import EntityPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.entity import Entity
from office365.sharepoint.internal.paths.static_operation import StaticOperationPath
from office365.sharepoint.tenant.administration.deny_add_and_customize_pages_status import (
    DenyAddAndCustomizePagesStatus,
)
from office365.sharepoint.tenant.administration.jobs.spo_operation import SpoOperation
from office365.sharepoint.tenant.administration.sharing_capabilities import (
    SharingCapabilities,
)
from office365.sharepoint.translation.resource_entry import SPResourceEntry


class SiteProperties(Entity):
    """Contains a property bag of information about a site."""

    def __repr__(self):
        return self.url or self.entity_type_name

    @staticmethod
    def clear_sharing_lock_down(context: ClientContext, site_url: str) -> SiteProperties:
        payload = {"siteUrl": site_url}
        binding_type = SiteProperties(context)
        qry = ServiceOperationQuery(binding_type, "ClearSharingLockDown", None, payload, None, None, True)
        context.add_query(qry)
        return binding_type

    def update(self) -> Self:
        """Updates the site collection properties with the new properties specified in the SiteProperties object."""

        def _update():
            super().update()

        self._ensure_site_path(_update)
        return self

    def update_ex(self) -> SpoOperation:
        """Updates the site collection properties with the new properties specified in the SiteProperties object."""
        return_type = SpoOperation(self.context)

        def _update_ex():
            qry = ServiceOperationQuery(self, "Update", parameters_type=self, return_type=return_type)
            self.context.add_query(qry)

        self._ensure_site_path(_update_ex)
        return return_type

    @property
    def allow_downloading_non_web_viewable_files(self) -> Optional[bool]:
        """Specifies if non web viewable files can be downloaded."""
        return self.properties.get("AllowDownloadingNonWebViewableFiles", None)

    @property
    def allow_editing(self) -> Optional[bool]:
        """Prevents users from editing Office files in the browser and copying and pasting Office file contents
        out of the browser window."""
        return self.properties.get("AllowEditing", None)

    @property
    def allow_self_service_upgrade(self) -> Optional[bool]:
        """Whether version to version upgrade is allowed on this site."""
        return self.properties.get("AllowSelfServiceUpgrade", None)

    @property
    def anonymous_link_expiration_in_days(self) -> Optional[int]:
        """Specifies all anonymous/anyone links that have been created
        (or will be created) will expire after the set number of days."""
        return self.properties.get("AnonymousLinkExpirationInDays", None)

    @property
    def apply_to_existing_document_libraries(self) -> Optional[bool]:
        """Create a job to apply the version history limits setting to existing document libraries."""
        return self.properties.get("ApplyToExistingDocumentLibraries", None)

    @property
    def apply_to_new_document_libraries(self) -> Optional[bool]:
        """Gets site version policy for new document libraries."""
        return self.properties.get("ApplyToNewDocumentLibraries", None)

    @property
    def archived_by(self) -> Optional[str]:
        """Gets site version policy for new document libraries."""
        return self.properties.get("ArchivedBy", None)

    @property
    def archived_time(self) -> Optional[datetime]:
        """Gets the time when site was archived."""
        return self.properties.get("ArchivedTime", datetime.min)

    @property
    def block_download_links_file_type(self) -> Optional[int]:
        """Block downloads for view-only files in SharePoint and OneDrive."""
        return self.properties.get("BlockDownloadLinksFileType", None)

    @property
    def block_download_microsoft365_group_ids(self) -> Optional[StringCollection]:
        """Block downloads for view-only files in SharePoint and OneDrive."""
        return self.properties.get("BlockDownloadMicrosoft365GroupIds", StringCollection())

    @property
    def block_download_policy_file_type_ids(self) -> Optional[StringCollection]:
        """"""
        return self.properties.get("BlockDownloadPolicyFileTypeIds", StringCollection())

    @property
    def created_time(self) -> Optional[datetime]:
        """Gets the time when the site was created."""
        return self.properties.get("CreatedTime", datetime.min)

    @property
    def deny_add_and_customize_pages(self) -> DenyAddAndCustomizePagesStatus:
        """Represents the status of the [DenyAddAndCustomizePages] feature on a site collection."""
        return self.properties.get("DenyAddAndCustomizePages", DenyAddAndCustomizePagesStatus.Unknown)

    @deny_add_and_customize_pages.setter
    def deny_add_and_customize_pages(self, value: DenyAddAndCustomizePagesStatus) -> None:
        """Sets the status of the [DenyAddAndCustomizePages] feature on a site collection."""
        self.set_property("DenyAddAndCustomizePages", value.value)

    @property
    def last_content_modified_date(self) -> Optional[datetime]:
        """Gets the last time content was modified on the site."""
        return self.properties.get("LastContentModifiedDate", datetime.min)

    @property
    def group_owner_login_name(self) -> Optional[str]:
        """Gets the Group Owner login name."""
        return self.properties.get("GroupOwnerLoginName", None)

    @property
    def is_hub_site(self) -> Optional[bool]:
        """"""
        return self.properties.get("IsHubSite", None)

    @property
    def title(self) -> Optional[str]:
        """Site title"""
        return self.properties.get("Title", None)

    @property
    def title_translations(self) -> ClientValueCollection[SPResourceEntry]:
        """Site titles"""
        return self.properties.get("TitleTranslations", ClientValueCollection(SPResourceEntry))

    @property
    def owner_login_name(self) -> Optional[str]:
        """ """
        return self.properties.get("OwnerLoginName", None)

    @property
    def webs_count(self) -> Optional[str]:
        """Gets the number of Web objects in the site."""
        return self.properties.get("WebsCount", None)

    @property
    def url(self) -> Optional[str]:
        """Gets the URL of the site."""
        return self.properties.get("Url", None)

    @property
    def compatibility_level(self) -> Optional[str]:
        """Gets the compatibility level of the site."""
        return self.properties.get("CompatibilityLevel", None)

    @property
    def lock_state(self) -> Optional[str]:
        """Gets or sets the lock state of the site."""
        return self.properties.get("LockState", None)

    @property
    def sharing_capability(self) -> Optional[SharingCapabilities]:
        """
        Determines what level of sharing is available for the site.

        The valid values are:
            - ExternalUserAndGuestSharing (default) - External user sharing (share by email) and guest link sharing
                 are both enabled.
            - Disabled - External user sharing (share by email) and guest link sharing are both disabled.
            - ExternalUserSharingOnly - External user sharing (share by email) is enabled, but guest link sharing
                 is disabled.
            - ExistingExternalUserSharingOnly - Only guests already in your organization's directory.
        """
        return self.properties.get("SharingCapability", SharingCapabilities.None_)

    @sharing_capability.setter
    def sharing_capability(self, value: SharingCapabilities) -> None:
        """Sets the level of sharing for the site."""
        self.set_property("SharingCapability", value)

    @property
    def time_zone_id(self) -> Optional[str]:
        """Gets the time zone ID of the site."""
        return self.properties.get("TimeZoneId", None)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteProperties"

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "ArchivedTime": self.archived_time,
                "CreatedTime": self.created_time,
                "DenyAddAndCustomizePages": self.deny_add_and_customize_pages,
                "LastContentModifiedDate": self.last_content_modified_date,
                "SharingCapability": self.sharing_capability,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)

    def set_property(self, name, value, persist_changes=True):
        super().set_property(name, value, persist_changes)
        # fallback: create a new resource path
        if name == "Url" and self._resource_path is None:
            self._resource_path = StaticOperationPath(self.entity_type_name, {"Url": value})
        return self

    def _ensure_site_path(self, action):
        if isinstance(self.resource_path, ServiceOperationPath):

            def _loaded(return_type: ListItem) -> None:
                site_id = return_type.properties.get("SiteId")
                self._resource_path = EntityPath(site_id, self.parent_collection.resource_path)
                action()

            self.context.tenant.get_site(self.url).after_execute(_loaded)
        else:
            action()
