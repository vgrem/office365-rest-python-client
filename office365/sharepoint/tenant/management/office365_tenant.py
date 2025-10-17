from datetime import datetime
from typing import Dict, Optional

from typing_extensions import Self

from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import GuidCollection, StringCollection
from office365.sharepoint.administration.orgassets.org_assets import OrgAssets
from office365.sharepoint.authpolicy.spjitdlppolicydata import SPJitDlpPolicyData
from office365.sharepoint.entity import Entity
from office365.sharepoint.principal.users.user import User
from office365.sharepoint.tenant.administration.siteinfo_for_site_picker import SiteInfoForSitePicker
from office365.sharepoint.tenant.administration.syntex.billing_context import SyntexBillingContext
from office365.sharepoint.tenant.administration.syntex.power_apps import SyntexPowerAppsEnvironmentsContext
from office365.sharepoint.tenant.administration.syntex.premiumfeaturesettings import SyntexPremiumFeatureSettings
from office365.sharepoint.tenant.administration.theme_properties import ThemeProperties
from office365.sharepoint.tenant.management.externalusers.results.get import GetExternalUsersResults
from office365.sharepoint.tenant.management.externalusers.results.remove import RemoveExternalUsersResults
from office365.sharepoint.tenant.management.externalusers.results.session_revocation import (
    SPOUserSessionRevocationResult,
)


class Office365Tenant(Entity):
    """Represents a SharePoint Online tenant."""

    def __init__(self, context):
        static_path = StaticPath("Microsoft.Online.SharePoint.TenantManagement.Office365Tenant")
        super().__init__(context, static_path)

    @property
    def addressbar_link_permission(self) -> Optional[int]:
        return self.properties.get("AddressbarLinkPermission", None)

    @property
    def allow_comments_text_on_email_enabled(self) -> Optional[bool]:
        return self.properties.get("AllowCommentsTextOnEmailEnabled", None)

    @property
    def allow_editing(self) -> Optional[bool]:
        return self.properties.get("AllowEditing", None)

    @property
    def ai_builder_site_info_list(self) -> ClientValueCollection[SiteInfoForSitePicker]:
        return self.properties.get("AIBuilderSiteInfoList", ClientValueCollection(SiteInfoForSitePicker))

    def add_tenant_cdn_origin(self, cdn_type: int, origin_url: str):
        """
        Configures a new origin to public or private CDN, on either Tenant level or on a single Site level.
        Effectively, a tenant admin points out to a document library, or a folder in the document library
        and requests that content in that library should be retrievable by using a CDN.

        You must have the SharePoint Admin role or Global Administrator role and be a site collection administrator
        to run the operation.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        :param str origin_url: Specifies a path to the doc library to be configured. It can be provided in two ways:
            relative path, or a mask.
        """
        payload = {"cdnType": cdn_type, "originUrl": origin_url}
        qry = ServiceOperationQuery(self, "AddTenantCdnOrigin", None, payload)
        self.context.add_query(qry)
        return self

    def disable_sharing_for_non_owners_of_site(self, site_url: str) -> Self:
        """
        Disables Sharing For Non Owners
        :param str site_url:
        """
        payload = {"siteUrl": site_url}
        qry = ServiceOperationQuery(self, "DisableSharingForNonOwnersOfSite", None, payload)
        self.context.add_query(qry)
        return self

    def get_tenant_cdn_enabled(self, cdn_type: int):
        """
        Returns whether Public content delivery network (CDN) or Private CDN is enabled on the tenant level.

        You must have the SharePoint Admin role or Global Administrator role and be a site collection administrator
        to run the operation.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        """
        payload = {"cdnType": cdn_type}
        return_type = ClientResult(self.context)
        qry = ServiceOperationQuery(self, "GetTenantCdnEnabled", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def set_block_download_file_type_policy_data(
        self,
        block_download_file_type_policy: bool,
        file_type_ids: list[int],
        excluded_block_download_group_ids: list[str],
    ) -> Self:
        """"""
        payload = {
            "blockDownloadFileTypePolicy": block_download_file_type_policy,
            "fileTypeIds": file_type_ids,
            "excludedBlockDownloadGroupIds": excluded_block_download_group_ids,
        }
        qry = ServiceOperationQuery(self, "SetBlockDownloadFileTypePolicyData", None, payload)
        self.context.add_query(qry)
        return self

    def set_tenant_cdn_enabled(self, cdn_type: int, is_enabled: bool) -> Self:
        """
        Enables or disables Public content delivery network (CDN) or Private CDN on the tenant level.

        You must have the SharePoint Admin role or Global Administrator role and be a site collection administrator
        to run the operation.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        :param bool is_enabled: Specifies if the CDN is enabled.
        """
        payload = {"cdnType": cdn_type, "isEnabled": is_enabled}
        qry = ServiceOperationQuery(self, "SetTenantCdnEnabled", None, payload)
        self.context.add_query(qry)
        return self

    def remove_tenant_cdn_origin(self, cdn_type, origin_url):
        """
        Removes a new origin from the Public or Private content delivery network (CDN).

        You must have the SharePoint Admin role or Global Administrator role and be a site collection administrator
        to run the operation.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        :param str origin_url: Specifies a path to the doc library to be configured. It can be provided in two ways:
            relative path, or a mask.
        """
        payload = {"cdnType": cdn_type, "originUrl": origin_url}
        qry = ServiceOperationQuery(self, "RemoveTenantCdnOrigin", None, payload)
        self.context.add_query(qry)
        return self

    def get_tenant_cdn_policies(self, cdn_type):
        """
        Get the public or private Policies applied on your SharePoint Online Tenant.

        Requires Tenant administrator permissions.


        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        """
        payload = {"cdnType": cdn_type}
        return_type = ClientResult(self.context, ClientValueCollection(str))
        qry = ServiceOperationQuery(self, "GetTenantCdnPolicies", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def set_tenant_cdn_policy(self, cdn_type, policy, policy_value):
        """
        Sets the content delivery network (CDN) policies at the tenant level.

        Requires Tenant administrator permissions.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        :param int policy: The PolicyType specifies the type of policy to set.
               Valid values:
                  IncludeFileExtensions
                  ExcludeRestrictedSiteClassifications
                  ExcludeIfNoScriptDisabled
        :param str policy_value: A String representing the value of the policy type defined by the PolicyType parameter.
        """
        payload = {"cdnType": cdn_type, "policy": policy, "policyValue": policy_value}
        qry = ServiceOperationQuery(self, "SetTenantCdnPolicy", None, payload)
        self.context.add_query(qry)
        return self

    def revoke_all_user_sessions(self, user):
        """
        Provides IT administrators the ability to invalidate a particular users' O365 sessions across all their devices.

        :param str or User user: Specifies a user name or user object
              (for example, user1@contoso.com) or User object
        """
        return_type = SPOUserSessionRevocationResult(self.context)

        def _revoke_all_user_sessions(login_name):
            """
            Logouts a user's sessions across all their devices

            :type login_name: str
            """
            qry = ServiceOperationQuery(self, "RevokeAllUserSessions", [login_name], None, None, return_type)
            self.context.add_query(qry)

        if isinstance(user, User):

            def _user_loaded():
                _revoke_all_user_sessions(user.login_name)

            user.ensure_property("LoginName", _user_loaded)
        else:
            _revoke_all_user_sessions(user)
        return return_type

    def get_external_users(self, position=0, page_size=50, _filter=None, sort_order=0):
        """
        Returns external users in the tenant.

        :param int position: Use to specify the zero-based index of the position in the sorted collection of the
                             first result to be returned.
        :param int page_size: Specifies the maximum number of users to be returned in the collection.
                              The value must be less than or equal to 50.
        :param str _filter: Limits the results to only those users whose first name, last name, or email address
                            begins with the text in the string using a case-insensitive comparison.
        :param int sort_order: Specifies the sort results in Ascending or Descending order on the User.Email property
                               should occur.
        """
        return_type = GetExternalUsersResults(self.context)
        payload = {"position": position, "pageSize": page_size, "filter": _filter, "sortOrder": sort_order}
        qry = ServiceOperationQuery(self, "GetExternalUsers", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def remove_external_users(self, unique_ids=None):
        """
        Removes a collection of external users from the tenancy's folder.

        :param list[str] unique_ids: Specifies an ID that can be used to identify an external user based on
                                     their Windows Live ID.
        """
        payload = {"uniqueIds": unique_ids}
        return_type = RemoveExternalUsersResults(self.context)
        qry = ServiceOperationQuery(self, "RemoveExternalUsers", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_all_tenant_themes(self):
        """
        Get all themes from tenant
        """
        return_type = ClientObjectCollection(self.context, ThemeProperties)
        qry = ServiceOperationQuery(self, "GetAllTenantThemes", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def add_tenant_theme(self, name: str, theme_json: str) -> ClientResult[bool]:
        """
        Adds a new theme to a tenant.

        :param str name:
        :param str theme_json:
        """
        return_type = ClientResult(self.context)
        payload = {"name": name, "themeJson": theme_json}
        qry = ServiceOperationQuery(self, "AddTenantTheme", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def delete_tenant_theme(self, name: str) -> Self:
        """
        Removes a theme from tenant
        :type name: str
        """
        payload = {"name": name}
        qry = ServiceOperationQuery(self, "DeleteTenantTheme", None, payload)
        self.context.add_query(qry)
        return self

    def queue_import_profile_properties(self, id_type, source_data_id_property, property_map, source_uri):
        """Bulk import custom user profile properties

        :param int id_type: The type of id to use when looking up the user profile.
        :param str source_data_id_property: The name of the ID property in the source data.
        :param dict property_map: A map from the source property name to the user profile service property name.
        :param str source_uri: The URI of the source data file to import.
        """
        return_type = ClientResult(self.context)
        payload = {
            "idType": id_type,
            "sourceDataIdProperty": source_data_id_property,
            "propertyMap": property_map,
            "sourceUri": source_uri,
        }
        qry = ServiceOperationQuery(self, "QueueImportProfileProperties", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def allow_anonymous_meeting_participants_to_access_whiteboards(self) -> Optional[int]:
        """Gets the AllowAnonymousMeetingParticipantsToAccessWhiteboards property"""
        return self.properties.get("AllowAnonymousMeetingParticipantsToAccessWhiteboards", None)

    @property
    def allow_downloading_non_web_viewable_files(self) -> Optional[bool]:
        """Gets the AllowDownloadingNonWebViewableFiles property"""
        return self.properties.get("AllowDownloadingNonWebViewableFiles", None)

    @property
    def allowed_domain_list_for_sync_client(self) -> GuidCollection:
        """Gets the AllowedDomainListForSyncClient property"""
        return self.properties.get("AllowedDomainListForSyncClient", GuidCollection())

    @property
    def allow_everyone_except_external_users_claim_in_private_site(self) -> Optional[bool]:
        """Gets the AllowEveryoneExceptExternalUsersClaimInPrivateSite property"""
        return self.properties.get("AllowEveryoneExceptExternalUsersClaimInPrivateSite", None)

    @property
    def allow_guest_user_share_to_users_not_in_site_collection(self) -> Optional[bool]:
        """Gets the AllowGuestUserShareToUsersNotInSiteCollection property"""
        return self.properties.get("AllowGuestUserShareToUsersNotInSiteCollection", None)

    @property
    def allow_legacy_browser_auth_protocols_enabled_setting(self) -> Optional[bool]:
        """Gets the AllowLegacyBrowserAuthProtocolsEnabledSetting property"""
        return self.properties.get("AllowLegacyBrowserAuthProtocolsEnabledSetting", None)

    @property
    def allow_limited_access_on_unmanaged_devices(self) -> Optional[bool]:
        """Gets the AllowLimitedAccessOnUnmanagedDevices property"""
        return self.properties.get("AllowLimitedAccessOnUnmanagedDevices", None)

    @property
    def allow_override_for_block_user_info_visibility(self) -> Optional[bool]:
        """Gets the AllowOverrideForBlockUserInfoVisibility property"""
        return self.properties.get("AllowOverrideForBlockUserInfoVisibility", None)

    @property
    def allow_select_security_groups_in_sp_sites_list(self) -> StringCollection:
        """Gets the AllowSelectSecurityGroupsInSPSitesList property"""
        return self.properties.get("AllowSelectSecurityGroupsInSPSitesList", StringCollection())

    @property
    def allow_select_s_gs_in_odb_list(self) -> StringCollection:
        """Gets the AllowSelectSGsInODBList property"""
        return self.properties.get("AllowSelectSGsInODBList", StringCollection())

    @property
    def allow_sharing_outside_restricted_access_control_groups(self) -> Optional[bool]:
        """Gets the AllowSharingOutsideRestrictedAccessControlGroups property"""
        return self.properties.get("AllowSharingOutsideRestrictedAccessControlGroups", None)

    @property
    def allow_web_property_bag_update_when_deny_add_and_customize_pages_is_enabled(self) -> Optional[bool]:
        """Gets the AllowWebPropertyBagUpdateWhenDenyAddAndCustomizePagesIsEnabled property"""
        return self.properties.get("AllowWebPropertyBagUpdateWhenDenyAddAndCustomizePagesIsEnabled", None)

    @property
    def anyone_link_track_users(self) -> Optional[bool]:
        """Gets the AnyoneLinkTrackUsers property"""
        return self.properties.get("AnyoneLinkTrackUsers", None)

    @property
    def app_access_information_barriers_allow_list(self) -> GuidCollection:
        """Gets the AppAccessInformationBarriersAllowList property"""
        return self.properties.get("AppAccessInformationBarriersAllowList", GuidCollection())

    @property
    def app_bypass_information_barriers(self) -> Optional[bool]:
        """Gets the AppBypassInformationBarriers property"""
        return self.properties.get("AppBypassInformationBarriers", None)

    @property
    def apply_app_enforced_restrictions_to_ad_hoc_recipients(self) -> Optional[bool]:
        """Gets the ApplyAppEnforcedRestrictionsToAdHocRecipients property"""
        return self.properties.get("ApplyAppEnforcedRestrictionsToAdHocRecipients", None)

    @property
    def app_only_bypass_people_picker_policies(self) -> Optional[bool]:
        """Gets the AppOnlyBypassPeoplePickerPolicies property"""
        return self.properties.get("AppOnlyBypassPeoplePickerPolicies", None)

    @property
    def auth_context_resilience_mode(self) -> Optional[int]:
        """Gets the AuthContextResilienceMode property"""
        return self.properties.get("AuthContextResilienceMode", None)

    @property
    def bcc_external_sharing_invitations(self) -> Optional[bool]:
        """Gets the BccExternalSharingInvitations property"""
        return self.properties.get("BccExternalSharingInvitations", None)

    @property
    def bcc_external_sharing_invitations_list(self) -> Optional[str]:
        """Gets the BccExternalSharingInvitationsList property"""
        return self.properties.get("BccExternalSharingInvitationsList", None)

    @property
    def block_access_on_unmanaged_devices(self) -> Optional[bool]:
        """Gets the BlockAccessOnUnmanagedDevices property"""
        return self.properties.get("BlockAccessOnUnmanagedDevices", None)

    @property
    def block_app_access_with_authentication_context(self) -> Optional[bool]:
        """Gets the BlockAppAccessWithAuthenticationContext property"""
        return self.properties.get("BlockAppAccessWithAuthenticationContext", None)

    @property
    def block_download_file_type_ids(self) -> ClientValueCollection[int]:
        """Gets the BlockDownloadFileTypeIds property"""
        return self.properties.get("BlockDownloadFileTypeIds", ClientValueCollection(int))

    @property
    def block_download_file_type_policy(self) -> Optional[bool]:
        """Gets the BlockDownloadFileTypePolicy property"""
        return self.properties.get("BlockDownloadFileTypePolicy", None)

    @property
    def block_download_links_file_type(self) -> Optional[int]:
        """Gets the BlockDownloadLinksFileType property"""
        return self.properties.get("BlockDownloadLinksFileType", None)

    @property
    def block_download_of_all_files_for_guests(self) -> Optional[bool]:
        """Gets the BlockDownloadOfAllFilesForGuests property"""
        return self.properties.get("BlockDownloadOfAllFilesForGuests", None)

    @property
    def block_download_of_all_files_on_unmanaged_devices(self) -> Optional[bool]:
        """Gets the BlockDownloadOfAllFilesOnUnmanagedDevices property"""
        return self.properties.get("BlockDownloadOfAllFilesOnUnmanagedDevices", None)

    @property
    def block_download_of_viewable_files_for_guests(self) -> Optional[bool]:
        """Gets the BlockDownloadOfViewableFilesForGuests property"""
        return self.properties.get("BlockDownloadOfViewableFilesForGuests", None)

    @property
    def block_download_of_viewable_files_on_unmanaged_devices(self) -> Optional[bool]:
        """Gets the BlockDownloadOfViewableFilesOnUnmanagedDevices property"""
        return self.properties.get("BlockDownloadOfViewableFilesOnUnmanagedDevices", None)

    @property
    def block_mac_sync(self) -> Optional[bool]:
        """Gets the BlockMacSync property"""
        return self.properties.get("BlockMacSync", None)

    @property
    def block_user_info_visibility(self) -> Optional[str]:
        """Gets the BlockUserInfoVisibility property"""
        return self.properties.get("BlockUserInfoVisibility", None)

    @property
    def block_user_info_visibility_in_one_drive(self) -> Optional[int]:
        """Gets the BlockUserInfoVisibilityInOneDrive property"""
        return self.properties.get("BlockUserInfoVisibilityInOneDrive", None)

    @property
    def block_user_info_visibility_in_share_point(self) -> Optional[int]:
        """Gets the BlockUserInfoVisibilityInSharePoint property"""
        return self.properties.get("BlockUserInfoVisibilityInSharePoint", None)

    @property
    def business_connectivity_service_disabled(self) -> Optional[bool]:
        """Gets the BusinessConnectivityServiceDisabled property"""
        return self.properties.get("BusinessConnectivityServiceDisabled", None)

    @property
    def comments_on_files_disabled(self) -> Optional[bool]:
        """Gets the CommentsOnFilesDisabled property"""
        return self.properties.get("CommentsOnFilesDisabled", None)

    @property
    def comments_on_list_items_disabled(self) -> Optional[bool]:
        """Gets the CommentsOnListItemsDisabled property"""
        return self.properties.get("CommentsOnListItemsDisabled", None)

    @property
    def comments_on_site_pages_disabled(self) -> Optional[bool]:
        """Gets the CommentsOnSitePagesDisabled property"""
        return self.properties.get("CommentsOnSitePagesDisabled", None)

    @property
    def conditional_access_policy(self) -> Optional[int]:
        """Gets the ConditionalAccessPolicy property"""
        return self.properties.get("ConditionalAccessPolicy", None)

    @property
    def conditional_access_policy_error_help_link(self) -> Optional[str]:
        """Gets the ConditionalAccessPolicyErrorHelpLink property"""
        return self.properties.get("ConditionalAccessPolicyErrorHelpLink", None)

    @property
    def content_type_sync_site_templates_list(self) -> StringCollection:
        """Gets the ContentTypeSyncSiteTemplatesList property"""
        return self.properties.get("ContentTypeSyncSiteTemplatesList", StringCollection())

    @property
    def core_block_guests_as_site_admin(self) -> Optional[int]:
        """Gets the CoreBlockGuestsAsSiteAdmin property"""
        return self.properties.get("CoreBlockGuestsAsSiteAdmin", None)

    @property
    def core_default_link_to_existing_access(self) -> Optional[bool]:
        """Gets the CoreDefaultLinkToExistingAccess property"""
        return self.properties.get("CoreDefaultLinkToExistingAccess", None)

    @property
    def core_default_share_link_role(self) -> Optional[int]:
        """Gets the CoreDefaultShareLinkRole property"""
        return self.properties.get("CoreDefaultShareLinkRole", None)

    @property
    def core_default_share_link_scope(self) -> Optional[int]:
        """Gets the CoreDefaultShareLinkScope property"""
        return self.properties.get("CoreDefaultShareLinkScope", None)

    @property
    def core_loop_default_sharing_link_role(self) -> Optional[int]:
        """Gets the CoreLoopDefaultSharingLinkRole property"""
        return self.properties.get("CoreLoopDefaultSharingLinkRole", None)

    @property
    def core_loop_default_sharing_link_scope(self) -> Optional[int]:
        """Gets the CoreLoopDefaultSharingLinkScope property"""
        return self.properties.get("CoreLoopDefaultSharingLinkScope", None)

    @property
    def core_request_files_link_enabled(self) -> Optional[bool]:
        """Gets the CoreRequestFilesLinkEnabled property"""
        return self.properties.get("CoreRequestFilesLinkEnabled", None)

    @property
    def core_request_files_link_expiration_in_days(self) -> Optional[int]:
        """Gets the CoreRequestFilesLinkExpirationInDays property"""
        return self.properties.get("CoreRequestFilesLinkExpirationInDays", None)

    @property
    def core_sharing_capability(self) -> Optional[int]:
        """Gets the CoreSharingCapability property"""
        return self.properties.get("CoreSharingCapability", None)

    @property
    def customized_external_sharing_service_url(self) -> Optional[str]:
        """Gets the CustomizedExternalSharingServiceUrl property"""
        return self.properties.get("CustomizedExternalSharingServiceUrl", None)

    @property
    def default_content_center_site(self) -> SiteInfoForSitePicker:
        """Gets the DefaultContentCenterSite property"""
        return self.properties.get("DefaultContentCenterSite", SiteInfoForSitePicker())

    @property
    def default_link_permission(self) -> Optional[int]:
        """Gets the DefaultLinkPermission property"""
        return self.properties.get("DefaultLinkPermission", None)

    @property
    def default_odb_mode(self) -> Optional[str]:
        """Gets the DefaultODBMode property"""
        return self.properties.get("DefaultODBMode", None)

    @property
    def default_sharing_link_type(self) -> Optional[int]:
        """Gets the DefaultSharingLinkType property"""
        return self.properties.get("DefaultSharingLinkType", None)

    @property
    def deny_select_security_groups_in_sp_sites_list(self) -> StringCollection:
        """Gets the DenySelectSecurityGroupsInSPSitesList property"""
        return self.properties.get("DenySelectSecurityGroupsInSPSitesList", StringCollection())

    @property
    def deny_select_s_gs_in_odb_list(self) -> StringCollection:
        """Gets the DenySelectSGsInODBList property"""
        return self.properties.get("DenySelectSGsInODBList", StringCollection())

    @property
    def disable_add_to_one_drive(self) -> Optional[bool]:
        """Gets the DisableAddToOneDrive property"""
        return self.properties.get("DisableAddToOneDrive", None)

    @property
    def disable_back_to_classic(self) -> Optional[bool]:
        """Gets the DisableBackToClassic property"""
        return self.properties.get("DisableBackToClassic", None)

    @property
    def disable_custom_app_authentication(self) -> Optional[bool]:
        """Gets the DisableCustomAppAuthentication property"""
        return self.properties.get("DisableCustomAppAuthentication", None)

    @property
    def disabled_modern_list_template_ids(self) -> GuidCollection:
        """Gets the DisabledModernListTemplateIds property"""
        return self.properties.get("DisabledModernListTemplateIds", GuidCollection())

    @property
    def disable_outlook_pst_version_trimming(self) -> Optional[bool]:
        """Gets the DisableOutlookPSTVersionTrimming property"""
        return self.properties.get("DisableOutlookPSTVersionTrimming", None)

    @property
    def disable_personal_list_creation(self) -> Optional[bool]:
        """Gets the DisablePersonalListCreation property"""
        return self.properties.get("DisablePersonalListCreation", None)

    @property
    def disable_spaces_activation(self) -> Optional[bool]:
        """Gets the DisableSpacesActivation property"""
        return self.properties.get("DisableSpacesActivation", None)

    @property
    def disable_viva_connections_analytics(self) -> Optional[bool]:
        """Gets the DisableVivaConnectionsAnalytics property"""
        return self.properties.get("DisableVivaConnectionsAnalytics", None)

    @property
    def display_start_a_site_option(self) -> Optional[bool]:
        """Gets the DisplayStartASiteOption property"""
        return self.properties.get("DisplayStartASiteOption", None)

    @property
    def email_attestation_enabled(self) -> Optional[bool]:
        """Gets the EmailAttestationEnabled property"""
        return self.properties.get("EmailAttestationEnabled", None)

    @property
    def email_attestation_re_auth_days(self) -> Optional[int]:
        """Gets the EmailAttestationReAuthDays property"""
        return self.properties.get("EmailAttestationReAuthDays", None)

    @property
    def email_attestation_required(self) -> Optional[bool]:
        """Gets the EmailAttestationRequired property"""
        return self.properties.get("EmailAttestationRequired", None)

    @property
    def enable_auto_expiration_version_trim(self) -> Optional[bool]:
        """Gets the EnableAutoExpirationVersionTrim property"""
        return self.properties.get("EnableAutoExpirationVersionTrim", None)

    @property
    def enable_auto_news_digest(self) -> Optional[bool]:
        """Gets the EnableAutoNewsDigest property"""
        return self.properties.get("EnableAutoNewsDigest", None)

    @property
    def enable_azure_adb2_b_integration(self) -> Optional[bool]:
        """Gets the EnableAzureADB2BIntegration property"""
        return self.properties.get("EnableAzureADB2BIntegration", None)

    @property
    def enable_guest_sign_in_acceleration(self) -> Optional[bool]:
        """Gets the EnableGuestSignInAcceleration property"""
        return self.properties.get("EnableGuestSignInAcceleration", None)

    @property
    def enable_promoted_file_handlers(self) -> Optional[bool]:
        """Gets the EnablePromotedFileHandlers property"""
        return self.properties.get("EnablePromotedFileHandlers", None)

    @property
    def enable_restricted_access_control(self) -> Optional[bool]:
        """Gets the EnableRestrictedAccessControl property"""
        return self.properties.get("EnableRestrictedAccessControl", None)

    @property
    def e_signature_app_list(self) -> StringCollection:
        """Gets the ESignatureAppList property"""
        return self.properties.get("ESignatureAppList", StringCollection())

    @property
    def e_signature_enabled(self) -> Optional[bool]:
        """Gets the ESignatureEnabled property"""
        return self.properties.get("ESignatureEnabled", None)

    @property
    def e_signature_site_info_list(self) -> ClientValueCollection[SiteInfoForSitePicker]:
        """Gets the ESignatureSiteInfoList property"""
        return self.properties.get("ESignatureSiteInfoList", ClientValueCollection(SiteInfoForSitePicker))

    @property
    def e_signature_site_list(self) -> GuidCollection:
        """Gets the ESignatureSiteList property"""
        return self.properties.get("ESignatureSiteList", GuidCollection())

    @property
    def e_signature_site_list_file_name(self) -> Optional[str]:
        """Gets the ESignatureSiteListFileName property"""
        return self.properties.get("ESignatureSiteListFileName", None)

    @property
    def e_signature_third_party_provider_info_list(self) -> StringCollection:
        """Gets the ESignatureThirdPartyProviderInfoList property"""
        return self.properties.get("ESignatureThirdPartyProviderInfoList", StringCollection())

    @property
    def e_signature_third_party_provider_list(self) -> StringCollection:
        """Gets the ESignatureThirdPartyProviderList property"""
        return self.properties.get("ESignatureThirdPartyProviderList", StringCollection())

    @property
    def e_signature_third_party_provider_list_file_name(self) -> Optional[str]:
        """Gets the ESignatureThirdPartyProviderListFileName property"""
        return self.properties.get("ESignatureThirdPartyProviderListFileName", None)

    @property
    def excluded_block_download_group_ids(self) -> GuidCollection:
        """Gets the ExcludedBlockDownloadGroupIds property"""
        return self.properties.get("ExcludedBlockDownloadGroupIds", GuidCollection())

    @property
    def excluded_file_extensions_for_sync_client(self) -> StringCollection:
        """Gets the ExcludedFileExtensionsForSyncClient property"""
        return self.properties.get("ExcludedFileExtensionsForSyncClient", StringCollection())

    @property
    def exempt_native_users_from_tenant_level_restriced_access_control(self) -> Optional[bool]:
        """Gets the ExemptNativeUsersFromTenantLevelRestricedAccessControl property"""
        return self.properties.get("ExemptNativeUsersFromTenantLevelRestricedAccessControl", None)

    @property
    def expire_versions_after_days(self) -> Optional[int]:
        """Gets the ExpireVersionsAfterDays property"""
        return self.properties.get("ExpireVersionsAfterDays", None)

    @property
    def external_services_enabled(self) -> Optional[bool]:
        """Gets the ExternalServicesEnabled property"""
        return self.properties.get("ExternalServicesEnabled", None)

    @property
    def external_user_expiration_required(self) -> Optional[bool]:
        """Gets the ExternalUserExpirationRequired property"""
        return self.properties.get("ExternalUserExpirationRequired", None)

    @property
    def external_user_expire_in_days(self) -> Optional[int]:
        """Gets the ExternalUserExpireInDays property"""
        return self.properties.get("ExternalUserExpireInDays", None)

    @property
    def file_anonymous_link_type(self) -> Optional[int]:
        """Gets the FileAnonymousLinkType property"""
        return self.properties.get("FileAnonymousLinkType", None)

    @property
    def file_picker_external_image_search_enabled(self) -> Optional[bool]:
        """Gets the FilePickerExternalImageSearchEnabled property"""
        return self.properties.get("FilePickerExternalImageSearchEnabled", None)

    @property
    def file_version_policy_xml(self) -> Optional[str]:
        """Gets the FileVersionPolicyXml property"""
        return self.properties.get("FileVersionPolicyXml", None)

    @property
    def folder_anonymous_link_type(self) -> Optional[int]:
        """Gets the FolderAnonymousLinkType property"""
        return self.properties.get("FolderAnonymousLinkType", None)

    @property
    def get_org_assets(self) -> OrgAssets:
        """Gets the GetOrgAssets property"""
        return self.properties.get("GetOrgAssets", OrgAssets())

    @property
    def guest_sharing_group_allow_list(self) -> Optional[str]:
        """Gets the GuestSharingGroupAllowList property"""
        return self.properties.get("GuestSharingGroupAllowList", None)

    @property
    def has_admin_completed_cu_configuration(self) -> Optional[bool]:
        """Gets the HasAdminCompletedCUConfiguration property"""
        return self.properties.get("HasAdminCompletedCUConfiguration", None)

    @property
    def hide_sync_button_on_doc_lib(self) -> Optional[bool]:
        """Gets the HideSyncButtonOnDocLib property"""
        return self.properties.get("HideSyncButtonOnDocLib", None)

    @property
    def hide_sync_button_on_odb(self) -> Optional[bool]:
        """Gets the HideSyncButtonOnODB property"""
        return self.properties.get("HideSyncButtonOnODB", None)

    @property
    def ib_implicit_group_based(self) -> Optional[bool]:
        """Gets the IBImplicitGroupBased property"""
        return self.properties.get("IBImplicitGroupBased", None)

    @property
    def image_tagging_option(self) -> Optional[int]:
        """Gets the ImageTaggingOption property"""
        return self.properties.get("ImageTaggingOption", None)

    @property
    def image_tagging_site_info_list(self) -> ClientValueCollection[SiteInfoForSitePicker]:
        """Gets the ImageTaggingSiteInfoList property"""
        return self.properties.get("ImageTaggingSiteInfoList", ClientValueCollection(SiteInfoForSitePicker))

    @property
    def image_tagging_site_list(self) -> GuidCollection:
        """Gets the ImageTaggingSiteList property"""
        return self.properties.get("ImageTaggingSiteList", GuidCollection())

    @property
    def image_tagging_site_list_file_name(self) -> Optional[str]:
        """Gets the ImageTaggingSiteListFileName property"""
        return self.properties.get("ImageTaggingSiteListFileName", None)

    @property
    def include_at_a_glance_in_share_emails(self) -> Optional[bool]:
        """Gets the IncludeAtAGlanceInShareEmails property"""
        return self.properties.get("IncludeAtAGlanceInShareEmails", None)

    @property
    def information_barriers_suspension(self) -> Optional[bool]:
        """Gets the InformationBarriersSuspension property"""
        return self.properties.get("InformationBarriersSuspension", None)

    @property
    def ip_address_allow_list(self) -> Optional[str]:
        """Gets the IPAddressAllowList property"""
        return self.properties.get("IPAddressAllowList", None)

    @property
    def ip_address_enforcement(self) -> Optional[bool]:
        """Gets the IPAddressEnforcement property"""
        return self.properties.get("IPAddressEnforcement", None)

    @property
    def ip_address_wac_token_lifetime(self) -> Optional[int]:
        """Gets the IPAddressWACTokenLifetime property"""
        return self.properties.get("IPAddressWACTokenLifetime", None)

    @property
    def is_unmanaged_sync_client_for_tenant_restricted(self) -> Optional[bool]:
        """Gets the IsUnmanagedSyncClientForTenantRestricted property"""
        return self.properties.get("IsUnmanagedSyncClientForTenantRestricted", None)

    @property
    def is_unmanaged_sync_client_restriction_flight_enabled(self) -> Optional[bool]:
        """Gets the IsUnmanagedSyncClientRestrictionFlightEnabled property"""
        return self.properties.get("IsUnmanagedSyncClientRestrictionFlightEnabled", None)

    @property
    def legacy_auth_protocols_enabled(self) -> Optional[bool]:
        """Gets the LegacyAuthProtocolsEnabled property"""
        return self.properties.get("LegacyAuthProtocolsEnabled", None)

    @property
    def legacy_browser_auth_protocols_enabled(self) -> Optional[bool]:
        """Gets the LegacyBrowserAuthProtocolsEnabled property"""
        return self.properties.get("LegacyBrowserAuthProtocolsEnabled", None)

    @property
    def limited_access_file_type(self) -> Optional[int]:
        """Gets the LimitedAccessFileType property"""
        return self.properties.get("LimitedAccessFileType", None)

    @property
    def machine_learning_capture_enabled(self) -> Optional[bool]:
        """Gets the MachineLearningCaptureEnabled property"""
        return self.properties.get("MachineLearningCaptureEnabled", None)

    @property
    def major_version_limit(self) -> Optional[int]:
        """Gets the MajorVersionLimit property"""
        return self.properties.get("MajorVersionLimit", None)

    @property
    def mark_all_files_as_sensitive_by_default(self) -> Optional[bool]:
        """Gets the MarkAllFilesAsSensitiveByDefault property"""
        return self.properties.get("MarkAllFilesAsSensitiveByDefault", None)

    @property
    def mass_delete_notification_disabled(self) -> Optional[bool]:
        """Gets the MassDeleteNotificationDisabled property"""
        return self.properties.get("MassDeleteNotificationDisabled", None)

    @property
    def media_transcription(self) -> Optional[int]:
        """Gets the MediaTranscription property"""
        return self.properties.get("MediaTranscription", None)

    @property
    def media_transcription_automatic_features(self) -> Optional[int]:
        """Gets the MediaTranscriptionAutomaticFeatures property"""
        return self.properties.get("MediaTranscriptionAutomaticFeatures", None)

    @property
    def mobile_friendly_url_enabled(self) -> Optional[bool]:
        """Gets the MobileFriendlyUrlEnabled property"""
        return self.properties.get("MobileFriendlyUrlEnabled", None)

    @property
    def my_sites_public_enabled(self) -> Optional[bool]:
        """Gets the MySitesPublicEnabled property"""
        return self.properties.get("MySitesPublicEnabled", None)

    @property
    def notifications_in_one_drive_for_business_enabled(self) -> Optional[bool]:
        """Gets the NotificationsInOneDriveForBusinessEnabled property"""
        return self.properties.get("NotificationsInOneDriveForBusinessEnabled", None)

    @property
    def notifications_in_share_point_enabled(self) -> Optional[bool]:
        """Gets the NotificationsInSharePointEnabled property"""
        return self.properties.get("NotificationsInSharePointEnabled", None)

    @property
    def notify_owners_when_items_reshared(self) -> Optional[bool]:
        """Gets the NotifyOwnersWhenItemsReshared property"""
        return self.properties.get("NotifyOwnersWhenItemsReshared", None)

    @property
    def odb_access_requests(self) -> Optional[int]:
        """Gets the ODBAccessRequests property"""
        return self.properties.get("ODBAccessRequests", None)

    @property
    def odb_members_can_share(self) -> Optional[int]:
        """Gets the ODBMembersCanShare property"""
        return self.properties.get("ODBMembersCanShare", None)

    @property
    def odb_sensitivity_refresh_window_in_hours(self) -> Optional[int]:
        """Gets the ODBSensitivityRefreshWindowInHours property"""
        return self.properties.get("ODBSensitivityRefreshWindowInHours", None)

    @property
    def odb_sharing_capability(self) -> Optional[int]:
        """Gets the ODBSharingCapability property"""
        return self.properties.get("ODBSharingCapability", None)

    @property
    def office_client_adal_disabled(self) -> Optional[bool]:
        """Gets the OfficeClientADALDisabled property"""
        return self.properties.get("OfficeClientADALDisabled", None)

    @property
    def one_drive_block_guests_as_site_admin(self) -> Optional[int]:
        """Gets the OneDriveBlockGuestsAsSiteAdmin property"""
        return self.properties.get("OneDriveBlockGuestsAsSiteAdmin", None)

    @property
    def one_drive_default_link_to_existing_access(self) -> Optional[bool]:
        """Gets the OneDriveDefaultLinkToExistingAccess property"""
        return self.properties.get("OneDriveDefaultLinkToExistingAccess", None)

    @property
    def one_drive_default_share_link_role(self) -> Optional[int]:
        """Gets the OneDriveDefaultShareLinkRole property"""
        return self.properties.get("OneDriveDefaultShareLinkRole", None)

    @property
    def one_drive_default_share_link_scope(self) -> Optional[int]:
        """Gets the OneDriveDefaultShareLinkScope property"""
        return self.properties.get("OneDriveDefaultShareLinkScope", None)

    @property
    def one_drive_for_guests_enabled(self) -> Optional[bool]:
        """Gets the OneDriveForGuestsEnabled property"""
        return self.properties.get("OneDriveForGuestsEnabled", None)

    @property
    def one_drive_loop_default_sharing_link_role(self) -> Optional[int]:
        """Gets the OneDriveLoopDefaultSharingLinkRole property"""
        return self.properties.get("OneDriveLoopDefaultSharingLinkRole", None)

    @property
    def one_drive_loop_default_sharing_link_scope(self) -> Optional[int]:
        """Gets the OneDriveLoopDefaultSharingLinkScope property"""
        return self.properties.get("OneDriveLoopDefaultSharingLinkScope", None)

    @property
    def one_drive_request_files_link_enabled(self) -> Optional[bool]:
        """Gets the OneDriveRequestFilesLinkEnabled property"""
        return self.properties.get("OneDriveRequestFilesLinkEnabled", None)

    @property
    def one_drive_request_files_link_expiration_in_days(self) -> Optional[int]:
        """Gets the OneDriveRequestFilesLinkExpirationInDays property"""
        return self.properties.get("OneDriveRequestFilesLinkExpirationInDays", None)

    @property
    def owner_anonymous_notification(self) -> Optional[bool]:
        """Gets the OwnerAnonymousNotification property"""
        return self.properties.get("OwnerAnonymousNotification", None)

    @property
    def prevent_external_users_from_resharing(self) -> Optional[bool]:
        """Gets the PreventExternalUsersFromResharing property"""
        return self.properties.get("PreventExternalUsersFromResharing", None)

    @property
    def provision_shared_with_everyone_folder(self) -> Optional[bool]:
        """Gets the ProvisionSharedWithEveryoneFolder property"""
        return self.properties.get("ProvisionSharedWithEveryoneFolder", None)

    @property
    def public_cdn_allowed_file_types(self) -> Optional[str]:
        """Gets the PublicCdnAllowedFileTypes property"""
        return self.properties.get("PublicCdnAllowedFileTypes", None)

    @property
    def public_cdn_enabled(self) -> Optional[bool]:
        """Gets the PublicCdnEnabled property"""
        return self.properties.get("PublicCdnEnabled", None)

    @property
    def public_cdn_origins(self) -> StringCollection:
        """Gets the PublicCdnOrigins property"""
        return self.properties.get("PublicCdnOrigins", StringCollection())

    @property
    def recycle_bin_retention_period(self) -> Optional[int]:
        """Gets the RecycleBinRetentionPeriod property"""
        return self.properties.get("RecycleBinRetentionPeriod", None)

    @property
    def reduce_temp_token_lifetime_enabled(self) -> Optional[bool]:
        """Gets the ReduceTempTokenLifetimeEnabled property"""
        return self.properties.get("ReduceTempTokenLifetimeEnabled", None)

    @property
    def reduce_temp_token_lifetime_value(self) -> Optional[int]:
        """Gets the ReduceTempTokenLifetimeValue property"""
        return self.properties.get("ReduceTempTokenLifetimeValue", None)

    @property
    def require_anonymous_links_expire_in_days(self) -> Optional[int]:
        """Gets the RequireAnonymousLinksExpireInDays property"""
        return self.properties.get("RequireAnonymousLinksExpireInDays", None)

    @property
    def require_organization_links_expire_in_days(self) -> Optional[int]:
        """Gets the RequireOrganizationLinksExpireInDays property"""
        return self.properties.get("RequireOrganizationLinksExpireInDays", None)

    @property
    def restricted_access_control_for_one_drive_error_help_link(self) -> Optional[str]:
        """Gets the RestrictedAccessControlForOneDriveErrorHelpLink property"""
        return self.properties.get("RestrictedAccessControlForOneDriveErrorHelpLink", None)

    @property
    def restricted_access_controlfor_sites_error_help_link(self) -> Optional[str]:
        """Gets the RestrictedAccessControlforSitesErrorHelpLink property"""
        return self.properties.get("RestrictedAccessControlforSitesErrorHelpLink", None)

    @property
    def search_resolve_exact_email_or_upn(self) -> Optional[bool]:
        """Gets the SearchResolveExactEmailOrUPN property"""
        return self.properties.get("SearchResolveExactEmailOrUPN", None)

    @property
    def self_service_site_creation_disabled(self) -> Optional[bool]:
        """Gets the SelfServiceSiteCreationDisabled property"""
        return self.properties.get("SelfServiceSiteCreationDisabled", None)

    @property
    def sharing_allowed_domain_list(self) -> Optional[str]:
        """Gets the SharingAllowedDomainList property"""
        return self.properties.get("SharingAllowedDomainList", None)

    @property
    def sharing_blocked_domain_list(self) -> Optional[str]:
        """Gets the SharingBlockedDomainList property"""
        return self.properties.get("SharingBlockedDomainList", None)

    @property
    def sharing_capability(self) -> Optional[int]:
        """Gets the SharingCapability property"""
        return self.properties.get("SharingCapability", None)

    @property
    def sharing_domain_restriction_mode(self) -> Optional[int]:
        """Gets the SharingDomainRestrictionMode property"""
        return self.properties.get("SharingDomainRestrictionMode", None)

    @property
    def show_all_users_claim(self) -> Optional[bool]:
        """Gets the ShowAllUsersClaim property"""
        return self.properties.get("ShowAllUsersClaim", None)

    @property
    def show_everyone_claim(self) -> Optional[bool]:
        """Gets the ShowEveryoneClaim property"""
        return self.properties.get("ShowEveryoneClaim", None)

    @property
    def show_everyone_except_external_users_claim(self) -> Optional[bool]:
        """Gets the ShowEveryoneExceptExternalUsersClaim property"""
        return self.properties.get("ShowEveryoneExceptExternalUsersClaim", None)

    @property
    def show_ngsc_dialog_for_sync_on_odb(self) -> Optional[bool]:
        """Gets the ShowNGSCDialogForSyncOnODB property"""
        return self.properties.get("ShowNGSCDialogForSyncOnODB", None)

    @property
    def show_open_in_desktop_option_for_synced_files(self) -> Optional[bool]:
        """Gets the ShowOpenInDesktopOptionForSyncedFiles property"""
        return self.properties.get("ShowOpenInDesktopOptionForSyncedFiles", None)

    @property
    def show_people_picker_group_suggestions_for_ib(self) -> Optional[bool]:
        """Gets the ShowPeoplePickerGroupSuggestionsForIB property"""
        return self.properties.get("ShowPeoplePickerGroupSuggestionsForIB", None)

    @property
    def show_people_picker_suggestions_for_guest_users(self) -> Optional[bool]:
        """Gets the ShowPeoplePickerSuggestionsForGuestUsers property"""
        return self.properties.get("ShowPeoplePickerSuggestionsForGuestUsers", None)

    @property
    def sign_in_acceleration_domain(self) -> Optional[str]:
        """Gets the SignInAccelerationDomain property"""
        return self.properties.get("SignInAccelerationDomain", None)

    @property
    def site_owner_manage_legacy_service_principal_enabled(self) -> Optional[bool]:
        """Gets the SiteOwnerManageLegacyServicePrincipalEnabled property"""
        return self.properties.get("SiteOwnerManageLegacyServicePrincipalEnabled", None)

    @property
    def social_bar_on_site_pages_disabled(self) -> Optional[bool]:
        """Gets the SocialBarOnSitePagesDisabled property"""
        return self.properties.get("SocialBarOnSitePagesDisabled", None)

    @property
    def sp_jit_dlp_policy_data(self) -> SPJitDlpPolicyData:
        """Gets the SPJitDlpPolicyData property"""
        return self.properties.get("SPJitDlpPolicyData", SPJitDlpPolicyData())

    @property
    def start_a_site_form_url(self) -> Optional[str]:
        """Gets the StartASiteFormUrl property"""
        return self.properties.get("StartASiteFormUrl", None)

    @property
    def stop_new2010_workflows(self) -> Optional[bool]:
        """Gets the StopNew2010Workflows property"""
        return self.properties.get("StopNew2010Workflows", None)

    @property
    def stop_new2013_workflows(self) -> Optional[bool]:
        """Gets the StopNew2013Workflows property"""
        return self.properties.get("StopNew2013Workflows", None)

    @property
    def stream_launch_config(self) -> Optional[int]:
        """Gets the StreamLaunchConfig property"""
        return self.properties.get("StreamLaunchConfig", None)

    @property
    def stream_launch_config_last_updated(self) -> datetime:
        """Gets the StreamLaunchConfigLastUpdated property"""
        return self.properties.get("StreamLaunchConfigLastUpdated", datetime.min)

    @property
    def stream_launch_config_update_count(self) -> Optional[int]:
        """Gets the StreamLaunchConfigUpdateCount property"""
        return self.properties.get("StreamLaunchConfigUpdateCount", None)

    @property
    def sync_privacy_profile_properties(self) -> Optional[bool]:
        """Gets the SyncPrivacyProfileProperties property"""
        return self.properties.get("SyncPrivacyProfileProperties", None)

    @property
    def syntex_billing_subscription_settings(self) -> SyntexBillingContext:
        """Gets the SyntexBillingSubscriptionSettings property"""
        return self.properties.get("SyntexBillingSubscriptionSettings", SyntexBillingContext())

    @property
    def syntex_internal_feature_flags(self) -> Optional[Dict]:
        """Gets the SyntexInternalFeatureFlags property"""
        return self.properties.get("SyntexInternalFeatureFlags", None)

    @property
    def syntex_media_analytics_settings(self) -> SyntexPremiumFeatureSettings:
        """Gets the SyntexMediaAnalyticsSettings property"""
        return self.properties.get("SyntexMediaAnalyticsSettings", SyntexPremiumFeatureSettings())

    @property
    def syntex_payg_feature_activations(self) -> Optional[dict]:
        """Gets the SyntexPaygFeatureActivations property"""
        return self.properties.get("SyntexPaygFeatureActivations", None)

    @property
    def syntex_playback_transcript_translation_settings(self) -> SyntexPremiumFeatureSettings:
        """Gets the SyntexPlaybackTranscriptTranslationSettings property"""
        return self.properties.get("SyntexPlaybackTranscriptTranslationSettings", SyntexPremiumFeatureSettings())

    @property
    def syntex_power_apps_environments_context(self) -> SyntexPowerAppsEnvironmentsContext:
        """Gets the SyntexPowerAppsEnvironmentsContext property"""
        return self.properties.get("SyntexPowerAppsEnvironmentsContext", SyntexPowerAppsEnvironmentsContext())

    @property
    def tls_token_binding_policy_value(self) -> Optional[int]:
        """Gets the TlsTokenBindingPolicyValue property"""
        return self.properties.get("TlsTokenBindingPolicyValue", None)

    @property
    def use_find_people_in_people_picker(self) -> Optional[bool]:
        """Gets the UseFindPeopleInPeoplePicker property"""
        return self.properties.get("UseFindPeopleInPeoplePicker", None)

    @property
    def use_persistent_cookies_for_explorer_view(self) -> Optional[bool]:
        """Gets the UsePersistentCookiesForExplorerView property"""
        return self.properties.get("UsePersistentCookiesForExplorerView", None)

    @property
    def viewers_can_comment_on_media_disabled(self) -> Optional[bool]:
        """Gets the ViewersCanCommentOnMediaDisabled property"""
        return self.properties.get("ViewersCanCommentOnMediaDisabled", None)

    @property
    def view_in_file_explorer_enabled(self) -> Optional[bool]:
        """Gets the ViewInFileExplorerEnabled property"""
        return self.properties.get("ViewInFileExplorerEnabled", None)

    @property
    def who_can_share_allow_list(self) -> Optional[str]:
        """Gets the WhoCanShareAllowList property"""
        return self.properties.get("WhoCanShareAllowList", None)

    @property
    def workflow2010_disabled(self) -> Optional[bool]:
        """Gets the Workflow2010Disabled property"""
        return self.properties.get("Workflow2010Disabled", None)

    @property
    def workflows2013_state(self) -> Optional[int]:
        """Gets the Workflows2013State property"""
        return self.properties.get("Workflows2013State", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantManagement.Office365Tenant"
