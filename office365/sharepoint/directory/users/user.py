from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.directory.my_groups_result import MyGroupsResult
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection

if TYPE_CHECKING:
    from office365.sharepoint.directory.groups.group import Group


class User(Entity):
    """Represents a user in the SharePoint Directory"""

    @odata(name="aboutMe")
    @property
    def about_me(self) -> Optional[str]:
        """Stores a short description or bio of the user."""
        return self.properties.get("aboutMe", None)

    @odata(name="accountEnabled")
    @property
    def account_enabled(self) -> Optional[bool]:
        """Gets weather the account is active (user can log in and access services) or not"""
        return self.properties.get("accountEnabled", None)

    def is_member_of(self, group_id: str) -> ClientResult[bool]:
        return_type = ClientResult(self.context)

        def _user_loaded():
            from office365.sharepoint.directory.helper import SPHelper

            SPHelper.is_member_of(self.context, self.properties["principalName"], group_id, return_type)

        self.ensure_property("principalName").after_execute(lambda _: _user_loaded())
        return return_type

    def get_my_groups(self) -> MyGroupsResult:
        """
        Retrieves information about groups that a user belongs to.
        """
        return_type = MyGroupsResult(self.context)

        def _get_my_groups():
            from office365.sharepoint.directory.helper import SPHelper

            SPHelper.get_my_groups(self.context, self.properties["principalName"], 0, 10, return_type)

        self.ensure_property("principalName").after_execute(lambda _: _get_my_groups())
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Directory.User"

    @odata(name="alias")
    @property
    def alias(self) -> Optional[str]:
        """Gets the alias property"""
        return self.properties.get("alias", None)

    @odata(name="birthday")
    @property
    def birthday(self) -> Optional[datetime]:
        """Gets the birthday property"""
        return self.properties.get("birthday", datetime.min)

    @odata(name="cellPhone")
    @property
    def cell_phone(self) -> Optional[str]:
        """Gets the cellPhone property"""
        return self.properties.get("cellPhone", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="fax")
    @property
    def fax(self) -> Optional[str]:
        """Gets the fax property"""
        return self.properties.get("fax", None)

    @odata(name="hireDate")
    @property
    def hire_date(self) -> Optional[datetime]:
        """Gets the hireDate property"""
        return self.properties.get("hireDate", datetime.min)

    @odata(name="homePhone")
    @property
    def home_phone(self) -> Optional[str]:
        """Gets the homePhone property"""
        return self.properties.get("homePhone", None)

    @odata(name="id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the id property"""
        return self.properties.get("id", None)

    @odata(name="interests")
    @property
    def interests(self) -> StringCollection:
        """Gets the interests property"""
        return self.properties.get("interests", StringCollection())

    @odata(name="mail")
    @property
    def mail(self) -> Optional[str]:
        """Gets the mail property"""
        return self.properties.get("mail", None)

    @odata(name="mySite")
    @property
    def my_site(self) -> Optional[str]:
        """Gets the mySite property"""
        return self.properties.get("mySite", None)

    @odata(name="netId")
    @property
    def net_id(self) -> Optional[str]:
        """Gets the netId property"""
        return self.properties.get("netId", None)

    @odata(name="officeGraphEnabled")
    @property
    def office_graph_enabled(self) -> Optional[bool]:
        """Gets the officeGraphEnabled property"""
        return self.properties.get("officeGraphEnabled", None)

    @odata(name="onPremiseSecurityIdentifier")
    @property
    def on_premise_security_identifier(self) -> Optional[str]:
        """Gets the onPremiseSecurityIdentifier property"""
        return self.properties.get("onPremiseSecurityIdentifier", None)

    @odata(name="pastProjects")
    @property
    def past_projects(self) -> StringCollection:
        """Gets the pastProjects property"""
        return self.properties.get("pastProjects", StringCollection())

    @odata(name="pointPublishingPersonalSiteUrl")
    @property
    def point_publishing_personal_site_url(self) -> Optional[str]:
        """Gets the pointPublishingPersonalSiteUrl property"""
        return self.properties.get("pointPublishingPersonalSiteUrl", None)

    @odata(name="preferredName")
    @property
    def preferred_name(self) -> Optional[str]:
        """Gets the preferredName property"""
        return self.properties.get("preferredName", None)

    @odata(name="principalName")
    @property
    def principal_name(self) -> Optional[str]:
        """Gets the principalName property"""
        return self.properties.get("principalName", None)

    @odata(name="responsibilities")
    @property
    def responsibilities(self) -> StringCollection:
        """Gets the responsibilities property"""
        return self.properties.get("responsibilities", StringCollection())

    @odata(name="schools")
    @property
    def schools(self) -> StringCollection:
        """Gets the schools property"""
        return self.properties.get("schools", StringCollection())

    @odata(name="serviceInfo")
    @property
    def service_info(self) -> StringCollection:
        """Gets the serviceInfo property"""
        return self.properties.get("serviceInfo", StringCollection())

    @odata(name="sharePointAddTopicHighlightFirstRun")
    @property
    def sharepoint_add_topic_highlight_first_run(self) -> Optional[bool]:
        """Gets the sharePointAddTopicHighlightFirstRun property"""
        return self.properties.get("sharePointAddTopicHighlightFirstRun", None)

    @odata(name="sharePointContentBarViewsTeachingBubble")
    @property
    def sharepoint_content_bar_views_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointContentBarViewsTeachingBubble property"""
        return self.properties.get("sharePointContentBarViewsTeachingBubble", None)

    @odata(name="sharePointConversationsLinkFirstRun", beta=True)
    @property
    def sharepoint_conversations_link_first_run(self) -> Optional[bool]:
        """Gets the sharePointConversationsLinkFirstRun property"""
        return self.properties.get("sharePointConversationsLinkFirstRun", None)

    @odata(name="sharePointFiltersPaneFirstRun", beta=True)
    @property
    def sharepoint_filters_pane_first_run(self) -> Optional[bool]:
        """Gets the sharePointFiltersPaneFirstRun property"""
        return self.properties.get("sharePointFiltersPaneFirstRun", None)

    @odata(name="sharePointFollowedDocumentsMigrated")
    @property
    def sharepoint_followed_documents_migrated(self) -> Optional[bool]:
        """Gets the sharePointFollowedDocumentsMigrated property"""
        return self.properties.get("sharePointFollowedDocumentsMigrated", None)

    @odata(name="sharePointFollowedSitesMigrated")
    @property
    def sharepoint_followed_sites_migrated(self) -> Optional[bool]:
        """Gets the sharePointFollowedSitesMigrated property"""
        return self.properties.get("sharePointFollowedSitesMigrated", None)

    @odata(name="sharePointFollowedSitesMigrated2")
    @property
    def sharepoint_followed_sites_migrated2(self) -> Optional[bool]:
        """Gets the sharePointFollowedSitesMigrated2 property"""
        return self.properties.get("sharePointFollowedSitesMigrated2", None)

    @odata(name="sharePointFollowedSitesMigratedToSPO")
    @property
    def sharepoint_followed_sites_migrated_to_spo(self) -> Optional[bool]:
        """Gets the sharePointFollowedSitesMigratedToSPO property"""
        return self.properties.get("sharePointFollowedSitesMigratedToSPO", None)

    @odata(name="sharePointHomeCreateNewsTeachingBubble")
    @property
    def sharepoint_home_create_news_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointHomeCreateNewsTeachingBubble property"""
        return self.properties.get("sharePointHomeCreateNewsTeachingBubble", None)

    @odata(name="sharePointHomeFirstRun")
    @property
    def sharepoint_home_first_run(self) -> Optional[bool]:
        """Gets the sharePointHomeFirstRun property"""
        return self.properties.get("sharePointHomeFirstRun", None)

    @odata(name="sharePointHomeMobileUpsell")
    @property
    def sharepoint_home_mobile_upsell(self) -> Optional[bool]:
        """Gets the sharePointHomeMobileUpsell property"""
        return self.properties.get("sharePointHomeMobileUpsell", None)

    @odata(name="sharePointHomeRefreshFirstRun")
    @property
    def sharepoint_home_refresh_first_run(self) -> Optional[bool]:
        """Gets the sharePointHomeRefreshFirstRun property"""
        return self.properties.get("sharePointHomeRefreshFirstRun", None)

    @odata(name="sharePointKnowledgeCenterFirstRun")
    @property
    def sharepoint_knowledge_center_first_run(self) -> Optional[bool]:
        """Gets the sharePointKnowledgeCenterFirstRun property"""
        return self.properties.get("sharePointKnowledgeCenterFirstRun", None)

    @odata(name="sharePointKnowledgeManagementTopicPageFirstRun")
    @property
    def sharepoint_knowledge_management_topic_page_first_run(self) -> Optional[bool]:
        """Gets the sharePointKnowledgeManagementTopicPageFirstRun property"""
        return self.properties.get("sharePointKnowledgeManagementTopicPageFirstRun", None)

    @odata(name="sharePointLibrariesFirstRun")
    @property
    def sharepoint_libraries_first_run(self) -> Optional[bool]:
        """Gets the sharePointLibrariesFirstRun property"""
        return self.properties.get("sharePointLibrariesFirstRun", None)

    @odata(name="sharePointListsFirstRun")
    @property
    def sharepoint_lists_first_run(self) -> Optional[bool]:
        """Gets the sharePointListsFirstRun property"""
        return self.properties.get("sharePointListsFirstRun", None)

    @odata(name="sharePointListsGoMobileFirstRun")
    @property
    def sharepoint_lists_go_mobile_first_run(self) -> Optional[bool]:
        """Gets the sharePointListsGoMobileFirstRun property"""
        return self.properties.get("sharePointListsGoMobileFirstRun", None)

    @odata(name="sharePointListsHomeFirstRun")
    @property
    def sharepoint_lists_home_first_run(self) -> Optional[bool]:
        """Gets the sharePointListsHomeFirstRun property"""
        return self.properties.get("sharePointListsHomeFirstRun", None)

    @odata(name="sharePointModernDocSetsFirstRun")
    @property
    def sharepoint_modern_doc_sets_first_run(self) -> Optional[bool]:
        """Gets the sharePointModernDocSetsFirstRun property"""
        return self.properties.get("sharePointModernDocSetsFirstRun", None)

    @odata(name="sharePointModernHomepageFirstRun")
    @property
    def sharepoint_modern_homepage_first_run(self) -> Optional[bool]:
        """Gets the sharePointModernHomepageFirstRun property"""
        return self.properties.get("sharePointModernHomepageFirstRun", None)

    @odata(name="sharePointNewsDigestTeachingBubble")
    @property
    def sharepoint_news_digest_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointNewsDigestTeachingBubble property"""
        return self.properties.get("sharePointNewsDigestTeachingBubble", None)

    @odata(name="sharePointNewsDigestTeachingBubbleHomePage")
    @property
    def sharepoint_news_digest_teaching_bubble_home_page(self) -> Optional[bool]:
        """Gets the sharePointNewsDigestTeachingBubbleHomePage property"""
        return self.properties.get("sharePointNewsDigestTeachingBubbleHomePage", None)

    @odata(name="sharePointOneDriveBusinessFirstRun")
    @property
    def sharepoint_onedrive_business_first_run(self) -> Optional[bool]:
        """Gets the sharePointOneDriveBusinessFirstRun property"""
        return self.properties.get("sharePointOneDriveBusinessFirstRun", None)

    @odata(name="sharePointPageAuthoringFirstRun")
    @property
    def sharepoint_page_authoring_first_run(self) -> Optional[bool]:
        """Gets the sharePointPageAuthoringFirstRun property"""
        return self.properties.get("sharePointPageAuthoringFirstRun", None)

    @odata(name="sharePointPictureUrl")
    @property
    def sharepoint_picture_url(self) -> Optional[str]:
        """Gets the sharePointPictureUrl property"""
        return self.properties.get("sharePointPictureUrl", None)

    @odata(name="sharePointProfileId")
    @property
    def sharepoint_profile_id(self) -> Optional[UUID]:
        """Gets the sharePointProfileId property"""
        return self.properties.get("sharePointProfileId", None)

    @odata(name="sharePointSaveForLaterTeachingBubble")
    @property
    def sharepoint_save_for_later_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointSaveForLaterTeachingBubble property"""
        return self.properties.get("sharePointSaveForLaterTeachingBubble", None)

    @odata(name="sharePointTeamsTeachingBubble")
    @property
    def sharepoint_teams_teaching_bubble(self) -> Optional[bool]:
        """Gets the sharePointTeamsTeachingBubble property"""
        return self.properties.get("sharePointTeamsTeachingBubble", None)

    @odata(name="sharePointTopicAutoHighlightFirstRun")
    @property
    def sharepoint_topic_auto_highlight_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicAutoHighlightFirstRun property"""
        return self.properties.get("sharePointTopicAutoHighlightFirstRun", None)

    @odata(name="sharePointTopicManualHighlightFirstRun")
    @property
    def sharepoint_topic_manual_highlight_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicManualHighlightFirstRun property"""
        return self.properties.get("sharePointTopicManualHighlightFirstRun", None)

    @odata(name="sharePointTopicPageEditFirstRun")
    @property
    def sharepoint_topic_page_edit_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicPageEditFirstRun property"""
        return self.properties.get("sharePointTopicPageEditFirstRun", None)

    @odata(name="sharePointTopicPagePrivacyPermissionFirstRun")
    @property
    def sharepoint_topic_page_privacy_permission_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicPagePrivacyPermissionFirstRun property"""
        return self.properties.get("sharePointTopicPagePrivacyPermissionFirstRun", None)

    @odata(name="sharePointTopicPagePublishFirstRun")
    @property
    def sharepoint_topic_page_publish_first_run(self) -> Optional[bool]:
        """Gets the sharePointTopicPagePublishFirstRun property"""
        return self.properties.get("sharePointTopicPagePublishFirstRun", None)

    @odata(name="skills")
    @property
    def skills(self) -> StringCollection:
        """Gets the skills property"""
        return self.properties.get("skills", StringCollection())

    @odata(name="tags")
    @property
    def tags(self) -> StringCollection:
        """Gets the tags property"""
        return self.properties.get("tags", StringCollection())

    @odata(name="tenantInstanceId")
    @property
    def tenant_instance_id(self) -> Optional[UUID]:
        """Gets the tenantInstanceId property"""
        return self.properties.get("tenantInstanceId", None)

    @odata(name="userType")
    @property
    def user_type(self) -> Optional[str]:
        """Gets the userType property"""
        return self.properties.get("userType", None)

    @odata(name="membership", navigation=True)
    @property
    def membership(self) -> EntityCollection[Group]:
        """Gets the membership property"""
        from office365.sharepoint.directory.groups.group import Group

        return self.properties.get(
            "membership", EntityCollection[Group](self.context, Group, ResourcePath("membership", self.resource_path))
        )

    @odata(name="ownership", navigation=True)
    @property
    def ownership(self) -> EntityCollection[Group]:
        """Gets the ownership property"""
        from office365.sharepoint.directory.groups.group import Group

        return self.properties.get(
            "ownership", EntityCollection[Group](self.context, Group, ResourcePath("ownership", self.resource_path))
        )

    @odata(name="rankedMembership", navigation=True)
    @property
    def ranked_membership(self) -> EntityCollection[Group]:
        """Gets the rankedMembership property"""
        from office365.sharepoint.directory.groups.group import Group

        return self.properties.get(
            "rankedMembership",
            EntityCollection[Group](self.context, Group, ResourcePath("rankedMembership", self.resource_path)),
        )

    def check_member_groups(self, group_ids: str) -> Self:
        """CheckMemberGroups operation.

        Args:
            group_ids (str):
                groupIds parameter
        """
        qry = FunctionQuery(self, "CheckMemberGroups", [group_ids], None)
        self.context.add_query(qry)
        return self
