from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.administration.commentsonsitepagesdisabled import CommentsOnSitePagesDisabled
from office365.sharepoint.tenant.administration.customformurl import CustomFormUrl
from office365.sharepoint.tenant.administration.includeataglanceinshareemails import IncludeAtAGlanceInShareEmails
from office365.sharepoint.tenant.administration.mailfromaddress import MailFromAddress
from office365.sharepoint.tenant.administration.mobilenotificationisenabledforsharepoint import (  # noqa: E501
    MobileNotificationIsEnabledForSharepoint,
)
from office365.sharepoint.tenant.administration.newsitemanagedpath import NewSiteManagedPath
from office365.sharepoint.tenant.administration.newsubsiteinmodernoffforall import NewSubsiteInModernOffForAll
from office365.sharepoint.tenant.administration.newsubsiteinmodernoffformoderntemplates import (  # noqa: E501
    NewSubsiteInModernOffForModernTemplates,
)
from office365.sharepoint.tenant.administration.newteamsitemanagedpath import NewTeamSiteManagedPath
from office365.sharepoint.tenant.administration.parentsiteurl import ParentSiteUrl
from office365.sharepoint.tenant.administration.policyoption import PolicyOption
from office365.sharepoint.tenant.administration.requiresecondarycontact import RequireSecondaryContact
from office365.sharepoint.tenant.administration.settings.default_time_zone_id import (
    TenantDefaultTimeZoneId,
)
from office365.sharepoint.tenant.administration.shownextgenerationsyncclientonteamsite import (  # noqa: E501
    ShowNextGenerationSyncClientOnTeamSite,
)
from office365.sharepoint.tenant.administration.showselfservicesitecreation import ShowSelfServiceSiteCreation
from office365.sharepoint.tenant.administration.sitecreationnewux import SiteCreationNewUX
from office365.sharepoint.tenant.administration.sitepagesenabled import SitePagesEnabled
from office365.sharepoint.tenant.administration.sites.creation_default_storage_quota import (  # noqa: E501
    SiteCreationDefaultStorageQuota,
)
from office365.sharepoint.tenant.administration.smtp_server import SmtpServer
from office365.sharepoint.tenant.administration.splistmodernuxoff import SPListModernUXOff
from office365.sharepoint.tenant.administration.types import (
    AutoQuotaEnabled,
    DisableGroupify,
    DisableSelfServiceSiteCreation,
    EnableAutoNewsDigest,
)
from office365.sharepoint.tenantadministration.container_auto_quota_enabled import ContainerAutoQuotaEnabled

if TYPE_CHECKING:
    from office365.sharepoint.tenant.administration.settings.dataproperty import (
        SettingDataProperty,
    )


class TenantAdminSettingsService(Entity):
    """Manage various tenant-level settings related to SharePoint administration"""

    def __init__(self, context):
        static_path = ResourcePath("Microsoft.Online.SharePoint.TenantAdministration.TenantAdminSettingsService")
        super().__init__(context, static_path)

    def get_tenant_sharing_status(self) -> ClientResult[int]:
        """Retrieves the current state of sharing settings for a tenant"""
        return_type = ClientResult(self.context, int())
        qry = ServiceOperationQuery(self, "GetTenantSharingStatus", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="AutoQuotaEnabled", beta=True)
    @property
    def auto_quota_enabled(self):
        """Controls whether automatic quota management is enabled for SharePoint Online site collections.
        When this feature is enabled, SharePoint Online automatically adjusts the storage quota for site collections
        based on their usage, helping to ensure that site collections don't run out of space.
        """
        return self.properties.get("AutoQuotaEnabled", AutoQuotaEnabled())

    @odata(name="AvailableManagedPathsForSiteCreation", beta=True)
    @property
    def available_managed_paths_for_site_creation(self):
        """
        Specifies the managed paths that are available for the creation of new SharePoint sites within a tenant.
        """
        return self.properties.get("AvailableManagedPathsForSiteCreation", StringCollection())

    @odata(name="DisableGroupify", beta=True)
    @property
    def disable_groupify(self):
        """
        Controls whether SharePoint site owners in your tenant are allowed to convert classic SharePoint sites into
        Microsoft 365 Groups (a process commonly known as "groupifying" a site)
        """
        return self.properties.get("DisableGroupify", DisableGroupify())

    @odata(name="DisableSelfServiceSiteCreation", beta=True)
    @property
    def disable_self_service_site_creation(self):
        """ " """
        return self.properties.get("DisableSelfServiceSiteCreation", DisableSelfServiceSiteCreation())

    @odata(name="EnableAutoNewsDigest", beta=True)
    @property
    def enable_auto_news_digest(self):
        """ " """
        return self.properties.get("EnableAutoNewsDigest", EnableAutoNewsDigest())

    @odata(name="SmtpServer", beta=True)
    @property
    def smtp_server(self):
        """Specifies the server address or endpoint of the SMTP server that SharePoint Online or tenant-related
        services use for sending emails"""
        return self.properties.get("SmtpServer", SmtpServer())

    @odata(name="TenantDefaultTimeZoneId", beta=True)
    @property
    def tenant_default_time_zone_id(self):
        """Default time zone configured for a SharePoint Online tenant"""
        return self.properties.get("TenantDefaultTimeZoneId", TenantDefaultTimeZoneId())

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.TenantAdminSettingsService"

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "AvailableManagedPathsForSiteCreation": self.available_managed_paths_for_site_creation,
                "AutoQuotaEnabled": self.auto_quota_enabled,
                "DisableGroupify": self.disable_groupify,
                "DisableSelfServiceSiteCreation": self.disable_self_service_site_creation,
                "EnableAutoNewsDigest": self.enable_auto_news_digest,
                "SmtpServer": self.smtp_server,
                "TenantDefaultTimeZoneId": self.tenant_default_time_zone_id,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)

    @odata(name="CommentsOnSitePagesDisabled", beta=True)
    @property
    def comments_on_site_pages_disabled(self) -> CommentsOnSitePagesDisabled:
        """Gets the CommentsOnSitePagesDisabled property"""
        return self.properties.get("CommentsOnSitePagesDisabled", CommentsOnSitePagesDisabled())

    @odata(name="CustomFormUrl", beta=True)
    @property
    def custom_form_url(self) -> CustomFormUrl:
        """Gets the CustomFormUrl property"""
        return self.properties.get("CustomFormUrl", CustomFormUrl())

    @odata(name="IncludeAtAGlanceInShareEmails", beta=True)
    @property
    def include_at_a_glance_in_share_emails(self) -> IncludeAtAGlanceInShareEmails:
        """Gets the IncludeAtAGlanceInShareEmails property"""
        return self.properties.get("IncludeAtAGlanceInShareEmails", IncludeAtAGlanceInShareEmails())

    @odata(name="MailFromAddress", beta=True)
    @property
    def mail_from_address(self) -> MailFromAddress:
        """Gets the MailFromAddress property"""
        return self.properties.get("MailFromAddress", MailFromAddress())

    @odata(name="MobileNotificationIsEnabledForSharepoint", beta=True)
    @property
    def mobile_notification_is_enabled_for_sharepoint(self) -> MobileNotificationIsEnabledForSharepoint:
        """Gets the MobileNotificationIsEnabledForSharepoint property"""
        return self.properties.get(
            "MobileNotificationIsEnabledForSharepoint", MobileNotificationIsEnabledForSharepoint()
        )

    @odata(name="NewSiteManagedPath", beta=True)
    @property
    def new_site_managed_path(self) -> NewSiteManagedPath:
        """Gets the NewSiteManagedPath property"""
        return self.properties.get("NewSiteManagedPath", NewSiteManagedPath())

    @odata(name="NewSubsiteInModernOffForAll", beta=True)
    @property
    def new_subsite_in_modern_off_for_all(self) -> NewSubsiteInModernOffForAll:
        """Gets the NewSubsiteInModernOffForAll property"""
        return self.properties.get("NewSubsiteInModernOffForAll", NewSubsiteInModernOffForAll())

    @odata(name="NewSubsiteInModernOffForModernTemplates", beta=True)
    @property
    def new_subsite_in_modern_off_for_modern_templates(self) -> NewSubsiteInModernOffForModernTemplates:
        """Gets the NewSubsiteInModernOffForModernTemplates property"""
        return self.properties.get("NewSubsiteInModernOffForModernTemplates", NewSubsiteInModernOffForModernTemplates())

    @odata(name="NewTeamSiteManagedPath", beta=True)
    @property
    def new_team_site_managed_path(self) -> NewTeamSiteManagedPath:
        """Gets the NewTeamSiteManagedPath property"""
        return self.properties.get("NewTeamSiteManagedPath", NewTeamSiteManagedPath())

    @odata(name="ParentSiteUrl", beta=True)
    @property
    def parent_site_url(self) -> ParentSiteUrl:
        """Gets the ParentSiteUrl property"""
        return self.properties.get("ParentSiteUrl", ParentSiteUrl())

    @odata(name="PolicyOption", beta=True)
    @property
    def policy_option(self) -> PolicyOption:
        """Gets the PolicyOption property"""
        return self.properties.get("PolicyOption", PolicyOption())

    @odata(name="RequireSecondaryContact", beta=True)
    @property
    def require_secondary_contact(self) -> RequireSecondaryContact:
        """Gets the RequireSecondaryContact property"""
        return self.properties.get("RequireSecondaryContact", RequireSecondaryContact())

    @odata(name="ShowNextGenerationSyncClientOnTeamSite", beta=True)
    @property
    def show_next_generation_sync_client_on_team_site(self) -> ShowNextGenerationSyncClientOnTeamSite:
        """Gets the ShowNextGenerationSyncClientOnTeamSite property"""
        return self.properties.get("ShowNextGenerationSyncClientOnTeamSite", ShowNextGenerationSyncClientOnTeamSite())

    @odata(name="ShowSelfServiceSiteCreation", beta=True)
    @property
    def show_self_service_site_creation(self) -> ShowSelfServiceSiteCreation:
        """Gets the ShowSelfServiceSiteCreation property"""
        return self.properties.get("ShowSelfServiceSiteCreation", ShowSelfServiceSiteCreation())

    @odata(name="SiteCreationDefaultStorageQuota", beta=True)
    @property
    def site_creation_default_storage_quota(self) -> SiteCreationDefaultStorageQuota:
        """Gets the SiteCreationDefaultStorageQuota property"""
        return self.properties.get("SiteCreationDefaultStorageQuota", SiteCreationDefaultStorageQuota())

    @odata(name="SiteCreationNewUX", beta=True)
    @property
    def site_creation_new_ux(self) -> SiteCreationNewUX:
        """Gets the SiteCreationNewUX property"""
        return self.properties.get("SiteCreationNewUX", SiteCreationNewUX())

    @odata(name="SitePagesEnabled", beta=True)
    @property
    def site_pages_enabled(self) -> SitePagesEnabled:
        """Gets the SitePagesEnabled property"""
        return self.properties.get("SitePagesEnabled", SitePagesEnabled())

    @odata(name="SPListModernUXOff", beta=True)
    @property
    def sp_list_modern_ux_off(self) -> SPListModernUXOff:
        """Gets the SPListModernUXOff property"""
        return self.properties.get("SPListModernUXOff", SPListModernUXOff())

    def get_tenant_admin_sharepoint_settings_data(
        self, category: int
    ) -> ClientResult[ClientValueCollection[SettingDataProperty]]:
        """GetTenantAdminSharePointSettingsData operation.

        Args:
            category (int):
                category parameter
        """
        from office365.sharepoint.tenant.administration.settings.dataproperty import (
            SettingDataProperty,
        )

        return_type = ClientResult(self.context, ClientValueCollection[SettingDataProperty]())
        qry = ServiceOperationQuery(
            self, "GetTenantAdminSharePointSettingsData", None, {"category": category}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    @odata(name="ContainerAutoQuotaEnabled", beta=True)
    @property
    def container_auto_quota_enabled(self) -> Optional[ContainerAutoQuotaEnabled]:
        """Gets the ContainerAutoQuotaEnabled property"""
        return self.properties.get("ContainerAutoQuotaEnabled", None)
