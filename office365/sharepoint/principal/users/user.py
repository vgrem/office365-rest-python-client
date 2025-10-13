from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.alerts.collection import AlertCollection
from office365.sharepoint.principal.principal import Principal
from office365.sharepoint.principal.users.id_info import UserIdInfo
from office365.sharepoint.userprofiles.person_properties import PersonProperties

if TYPE_CHECKING:
    from office365.sharepoint.sites.site import Site


class User(Principal):
    """Represents a user in Microsoft SharePoint Foundation. A user is a type of SP.Principal."""

    def get_personal_site(self) -> "Site":
        """Get personal site for a user"""
        from office365.sharepoint.sites.site import Site

        return_type = Site(self.context)

        def _person_props_loaded(person_props: PersonProperties) -> None:
            return_type.set_property("__siteUrl", person_props.personal_url)

        def _get_properties_for():
            self.context.people_manager.get_properties_for(self.login_name).after_execute(_person_props_loaded)

        self.ensure_property("LoginName", _get_properties_for)
        return return_type

    def get_recent_files(self, top: int = 100) -> ClientResult[str]:
        """"""
        from office365.sharepoint.files.recent_file_collection import RecentFileCollection

        return_type = RecentFileCollection.get_recent_files(self.context, top)
        return return_type

    def get_user_profile_properties(self, property_names: List[str] = None):
        """
        :param list[str] property_names:
        """
        from office365.sharepoint.userprofiles.properties_for_user import UserProfilePropertiesForUser

        return_type = UserProfilePropertiesForUser(self.context)

        def _user_loaded():
            return_type.set_property("PropertyNames", property_names)
            return_type.set_property("AccountName", self.user_principal_name)

        self.ensure_property("UserPrincipalName", _user_loaded)
        return return_type

    def expire(self) -> Self:
        """"""
        qry = ServiceOperationQuery(self, "Expire")
        self.context.add_query(qry)
        return self

    @property
    def aad_object_id(self) -> UserIdInfo:
        """Gets the information of the user that contains the user's name identifier and the issuer of the
        user's name identifier."""
        return self.properties.get("AadObjectId", UserIdInfo())

    @property
    def alerts(self) -> AlertCollection:
        """Gets site alerts for this user."""
        return self.properties.get("Alerts", AlertCollection(self.context, ResourcePath("Alerts", self.resource_path)))

    @property
    def groups(self):
        """Gets a collection of group objects that represents all of the groups for the user."""
        from office365.sharepoint.principal.groups.collection import GroupCollection

        return self.properties.get("Groups", GroupCollection(self.context, ResourcePath("Groups", self.resource_path)))

    @property
    def is_site_admin(self) -> Optional[bool]:
        """Gets a Boolean value that specifies whether the user is a site collection administrator."""
        return self.properties.get("IsSiteAdmin", None)

    @property
    def user_id(self) -> UserIdInfo:
        """Gets the information of the user that contains the user's name identifier and the issuer of the
        user's name identifier."""
        return self.properties.get("UserId", UserIdInfo())

    @property
    def email(self) -> Optional[str]:
        """
        Specifies the e-mail address of the user.
        It MUST NOT be NULL. Its length MUST be equal to or less than 255.
        """
        return self.properties.get("Email", None)

    @property
    def email_with_fallback(self) -> Optional[str]:
        return self.properties.get("EmailWithFallback", None)

    @property
    def expiration(self) -> Optional[str]:
        return self.properties.get("Expiration", None)

    @property
    def is_email_authentication_guest_user(self) -> Optional[bool]:
        """
        Indicates whether the User is a share by email guest user using time of access authentication.
        If this instance is an email authentication guest user, this value MUST be true, otherwise it MUST be false.
        """
        return self.properties.get("IsEmailAuthenticationGuestUser", None)

    @property
    def is_share_by_email_guest_user(self) -> Optional[bool]:
        """
        Gets a value indicating whether this User is a share by email guest user.
        If this instance is a share by email guest user, it's true; otherwise, false.
        """
        return self.properties.get("IsShareByEmailGuestUser", None)

    @property
    def user_principal_name(self) -> Optional[str]:
        """User principal name of the user that initiated the sign-in."""
        return self.properties.get("UserPrincipalName", None)

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {"AadObjectId": self.aad_object_id, "UserId": self.user_id}
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)

    @property
    def about_me(self) -> Optional[str]:
        """Gets the aboutMe property"""
        return self.properties.get("aboutMe", None)

    @property
    def account_enabled(self) -> Optional[bool]:
        """Gets the accountEnabled property"""
        return self.properties.get("accountEnabled", None)

    @property
    def alias(self) -> Optional[str]:
        """Gets the alias property"""
        return self.properties.get("alias", None)

    @property
    def birthday(self) -> datetime:
        """Gets the birthday property"""
        return self.properties.get("birthday", datetime.min)

    @property
    def cell_phone(self) -> Optional[str]:
        """Gets the cellPhone property"""
        return self.properties.get("cellPhone", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def fax(self) -> Optional[str]:
        """Gets the fax property"""
        return self.properties.get("fax", None)

    @property
    def hire_date(self) -> datetime:
        """Gets the hireDate property"""
        return self.properties.get("hireDate", datetime.min)

    @property
    def home_phone(self) -> Optional[str]:
        """Gets the homePhone property"""
        return self.properties.get("homePhone", None)

    @property
    def id_(self) -> Optional[UUID]:
        """Gets the id property"""
        return self.properties.get("id", None)

    @property
    def interests(self) -> StringCollection:
        """Gets the interests property"""
        return self.properties.get("interests", StringCollection())

    @property
    def mail(self) -> Optional[str]:
        """Gets the mail property"""
        return self.properties.get("mail", None)

    @property
    def my_site(self) -> Optional[str]:
        """Gets the mySite property"""
        return self.properties.get("mySite", None)

    @property
    def net_id(self) -> Optional[str]:
        """Gets the netId property"""
        return self.properties.get("netId", None)

    @property
    def office_graph_enabled(self) -> Optional[bool]:
        """Gets the officeGraphEnabled property"""
        return self.properties.get("officeGraphEnabled", None)

    @property
    def past_projects(self) -> StringCollection:
        """Gets the pastProjects property"""
        return self.properties.get("pastProjects", StringCollection())

    @property
    def point_publishing_personal_site_url(self) -> Optional[str]:
        """Gets the pointPublishingPersonalSiteUrl property"""
        return self.properties.get("pointPublishingPersonalSiteUrl", None)

    @property
    def preferred_name(self) -> Optional[str]:
        """Gets the preferredName property"""
        return self.properties.get("preferredName", None)

    @property
    def principal_name(self) -> Optional[str]:
        """Gets the principalName property"""
        return self.properties.get("principalName", None)

    @property
    def responsibilities(self) -> StringCollection:
        """Gets the responsibilities property"""
        return self.properties.get("responsibilities", StringCollection())

    @property
    def schools(self) -> StringCollection:
        """Gets the schools property"""
        return self.properties.get("schools", StringCollection())

    @property
    def share_point_add_topic_highlight_first_run(self) -> Optional[bool]:
        """Gets the sharePointAddTopicHighlightFirstRun property"""
        return self.properties.get("sharePointAddTopicHighlightFirstRun", None)

    @property
    def share_point_content_bar_views_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointContentBarViewsTeachingBubble property"""
        return self.properties.get("sharePointContentBarViewsTeachingBubble", None)

    @property
    def share_point_conversations_link_first_run(self) -> Optional[bool]:
        """Gets the sharePointConversationsLinkFirstRun property"""
        return self.properties.get("sharePointConversationsLinkFirstRun", None)

    @property
    def share_point_filters_pane_first_run(self) -> Optional[bool]:
        """Gets the sharePointFiltersPaneFirstRun property"""
        return self.properties.get("sharePointFiltersPaneFirstRun", None)

    @property
    def share_point_followed_documents_migrated(self) -> Optional[bool]:
        """Gets the sharePointFollowedDocumentsMigrated property"""
        return self.properties.get("sharePointFollowedDocumentsMigrated", None)

    @property
    def share_point_followed_sites_migrated(self) -> Optional[bool]:
        """Gets the sharePointFollowedSitesMigrated property"""
        return self.properties.get("sharePointFollowedSitesMigrated", None)

    @property
    def share_point_followed_sites_migrated2(self) -> Optional[bool]:
        """Gets the sharePointFollowedSitesMigrated2 property"""
        return self.properties.get("sharePointFollowedSitesMigrated2", None)

    @property
    def share_point_followed_sites_migrated_to_spo(self) -> Optional[bool]:
        """Gets the sharePointFollowedSitesMigratedToSPO property"""
        return self.properties.get("sharePointFollowedSitesMigratedToSPO", None)

    @property
    def share_point_home_create_news_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointHomeCreateNewsTeachingBubble property"""
        return self.properties.get("sharePointHomeCreateNewsTeachingBubble", None)

    @property
    def share_point_home_first_run(self) -> Optional[bool]:
        """Gets the sharePointHomeFirstRun property"""
        return self.properties.get("sharePointHomeFirstRun", None)

    @property
    def share_point_home_mobile_upsell(self) -> Optional[bool]:
        """Gets the sharePointHomeMobileUpsell property"""
        return self.properties.get("sharePointHomeMobileUpsell", None)

    @property
    def share_point_home_refresh_first_run(self) -> Optional[bool]:
        """Gets the sharePointHomeRefreshFirstRun property"""
        return self.properties.get("sharePointHomeRefreshFirstRun", None)

    @property
    def share_point_knowledge_center_first_run(self) -> Optional[bool]:
        """Gets the sharePointKnowledgeCenterFirstRun property"""
        return self.properties.get("sharePointKnowledgeCenterFirstRun", None)

    @property
    def share_point_knowledge_management_topic_page_first_run(self) -> Optional[bool]:
        """Gets the sharePointKnowledgeManagementTopicPageFirstRun property"""
        return self.properties.get("sharePointKnowledgeManagementTopicPageFirstRun", None)

    @property
    def share_point_libraries_first_run(self) -> Optional[bool]:
        """Gets the sharePointLibrariesFirstRun property"""
        return self.properties.get("sharePointLibrariesFirstRun", None)

    @property
    def share_point_lists_first_run(self) -> Optional[bool]:
        """Gets the sharePointListsFirstRun property"""
        return self.properties.get("sharePointListsFirstRun", None)

    @property
    def share_point_lists_go_mobile_first_run(self) -> Optional[bool]:
        """Gets the sharePointListsGoMobileFirstRun property"""
        return self.properties.get("sharePointListsGoMobileFirstRun", None)

    @property
    def share_point_lists_home_first_run(self) -> Optional[bool]:
        """Gets the sharePointListsHomeFirstRun property"""
        return self.properties.get("sharePointListsHomeFirstRun", None)

    @property
    def share_point_modern_doc_sets_first_run(self) -> Optional[bool]:
        """Gets the sharePointModernDocSetsFirstRun property"""
        return self.properties.get("sharePointModernDocSetsFirstRun", None)

    @property
    def share_point_modern_homepage_first_run(self) -> Optional[bool]:
        """Gets the sharePointModernHomepageFirstRun property"""
        return self.properties.get("sharePointModernHomepageFirstRun", None)

    @property
    def share_point_news_digest_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointNewsDigestTeachingBubble property"""
        return self.properties.get("sharePointNewsDigestTeachingBubble", None)

    @property
    def share_point_news_digest_teaching_bubble_home_page(self) -> Optional[bool]:
        """Gets the sharePointNewsDigestTeachingBubbleHomePage property"""
        return self.properties.get("sharePointNewsDigestTeachingBubbleHomePage", None)

    @property
    def share_point_one_drive_business_first_run(self) -> Optional[bool]:
        """Gets the sharePointOneDriveBusinessFirstRun property"""
        return self.properties.get("sharePointOneDriveBusinessFirstRun", None)

    @property
    def share_point_page_authoring_first_run(self) -> Optional[bool]:
        """Gets the sharePointPageAuthoringFirstRun property"""
        return self.properties.get("sharePointPageAuthoringFirstRun", None)

    @property
    def share_point_picture_url(self) -> Optional[str]:
        """Gets the sharePointPictureUrl property"""
        return self.properties.get("sharePointPictureUrl", None)

    @property
    def share_point_profile_id(self) -> Optional[UUID]:
        """Gets the sharePointProfileId property"""
        return self.properties.get("sharePointProfileId", None)

    @property
    def share_point_save_for_later_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointSaveForLaterTeachingBubble property"""
        return self.properties.get("sharePointSaveForLaterTeachingBubble", None)

    @property
    def share_point_teams_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointTeamsTeachingBubble property"""
        return self.properties.get("sharePointTeamsTeachingBubble", None)

    @property
    def share_point_topic_auto_highlight_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicAutoHighlightFirstRun property"""
        return self.properties.get("sharePointTopicAutoHighlightFirstRun", None)

    @property
    def share_point_topic_manual_highlight_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicManualHighlightFirstRun property"""
        return self.properties.get("sharePointTopicManualHighlightFirstRun", None)

    @property
    def share_point_topic_page_edit_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicPageEditFirstRun property"""
        return self.properties.get("sharePointTopicPageEditFirstRun", None)

    @property
    def share_point_topic_page_privacy_permission_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicPagePrivacyPermissionFirstRun property"""
        return self.properties.get("sharePointTopicPagePrivacyPermissionFirstRun", None)

    @property
    def share_point_topic_page_publish_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicPagePublishFirstRun property"""
        return self.properties.get("sharePointTopicPagePublishFirstRun", None)

    @property
    def skills(self) -> StringCollection:
        """Gets the skills property"""
        return self.properties.get("skills", StringCollection())

    @property
    def tags(self) -> StringCollection:
        """Gets the tags property"""
        return self.properties.get("tags", StringCollection())

    @property
    def tenant_instance_id(self) -> Optional[UUID]:
        """Gets the tenantInstanceId property"""
        return self.properties.get("tenantInstanceId", None)

    @property
    def user_type(self) -> Optional[str]:
        """Gets the userType property"""
        return self.properties.get("userType", None)

    @property
    def entity_type_name(self):
        return "SP.Directory.User"
