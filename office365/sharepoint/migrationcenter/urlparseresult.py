from typing import Optional
from uuid import UUID

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.migrationcenter.listinformation import SPListInformation


class UrlParseResult(Entity):

    @property
    def display_url(self) -> Optional[str]:
        """Gets the DisplayUrl property"""
        return self.properties.get("DisplayUrl", None)

    @property
    def error_code(self) -> Optional[str]:
        """Gets the ErrorCode property"""
        return self.properties.get("ErrorCode", None)

    @property
    def free_site_storage_bytes(self) -> Optional[int]:
        """Gets the FreeSiteStorageBytes property"""
        return self.properties.get("FreeSiteStorageBytes", None)

    @property
    def has_enough_site_storage(self) -> Optional[bool]:
        """Gets the HasEnoughSiteStorage property"""
        return self.properties.get("HasEnoughSiteStorage", None)

    @property
    def is_current_user_site_admin(self) -> Optional[bool]:
        """Gets the IsCurrentUserSiteAdmin property"""
        return self.properties.get("IsCurrentUserSiteAdmin", None)

    @property
    def is_personal_site(self) -> Optional[bool]:
        """Gets the IsPersonalSite property"""
        return self.properties.get("IsPersonalSite", None)

    @property
    def message(self) -> Optional[str]:
        """Gets the Message property"""
        return self.properties.get("Message", None)

    @property
    def original_url(self) -> Optional[str]:
        """Gets the OriginalUrl property"""
        return self.properties.get("OriginalUrl", None)

    @property
    def processing_milliseconds(self) -> Optional[int]:
        """Gets the ProcessingMilliseconds property"""
        return self.properties.get("ProcessingMilliseconds", None)

    @property
    def server_url(self) -> Optional[str]:
        """Gets the ServerUrl property"""
        return self.properties.get("ServerUrl", None)

    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def site_server_relative_url(self) -> Optional[str]:
        """Gets the SiteServerRelativeUrl property"""
        return self.properties.get("SiteServerRelativeUrl", None)

    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)

    @property
    def sp_list_info_list(self) -> ClientValueCollection[SPListInformation]:
        """Gets the SPListInfoList property"""
        return self.properties.get("SPListInfoList", ClientValueCollection(SPListInformation))

    @property
    def success(self) -> Optional[bool]:
        """Gets the Success property"""
        return self.properties.get("Success", None)

    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)

    @property
    def web_server_relative_url(self) -> Optional[str]:
        """Gets the WebServerRelativeUrl property"""
        return self.properties.get("WebServerRelativeUrl", None)

    @property
    def web_template_id(self) -> Optional[int]:
        """Gets the WebTemplateId property"""
        return self.properties.get("WebTemplateId", None)

    @property
    def web_url(self) -> Optional[str]:
        """Gets the WebUrl property"""
        return self.properties.get("WebUrl", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.UrlParseResult"
