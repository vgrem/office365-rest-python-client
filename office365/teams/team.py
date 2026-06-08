from datetime import datetime
from typing import Any, Dict, Optional

from typing_extensions import Self

from office365.directory.permissions.grants.resource_specific import ResourceSpecificPermissionGrant
from office365.directory.profile_photo import ProfilePhoto
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.teams.apps.installation import TeamsAppInstallation
from office365.teams.channels.channel import Channel
from office365.teams.channels.collection import ChannelCollection
from office365.teams.fun_settings import TeamFunSettings
from office365.teams.guest_settings import TeamGuestSettings
from office365.teams.members.conversation_collection import ConversationMemberCollection
from office365.teams.members.settings import TeamMemberSettings
from office365.teams.messaging_settings import TeamMessagingSettings
from office365.teams.operations.async_operation import TeamsAsyncOperation
from office365.teams.schedule.schedule import Schedule
from office365.teams.specialization import TeamSpecialization
from office365.teams.summary import TeamSummary
from office365.teams.teamwork.activity_topic import TeamworkActivityTopic
from office365.teams.teamwork.notification_recipient import TeamworkNotificationRecipient
from office365.teams.teamwork.tags.tag import TeamworkTag
from office365.teams.template import TeamsTemplate
from office365.teams.visibility_type import TeamVisibilityType


class Team(Entity):
    """A team in Microsoft Teams is a collection of channel objects. A channel represents a topic, and therefore a
    logical isolation of discussion, within a team."""

    def __str__(self):
        return self.display_name or self.entity_type_name

    def execute_query_and_wait(self):
        """
        Submit request(s) to the server and waits until operation is completed
        """

        def _loaded():
            self.operations[0].poll_for_status(status_type="succeeded")

        self.ensure_property("id").after_execute(lambda _: _loaded())
        self.context.execute_query()
        return self

    def delete_object(self, permanent_delete=False):
        """Deletes a team"""

        def _delete_object():
            assert self.id is not None
            group = self.context.groups[self.id]
            self.context.groups.add_child(group)
            group.delete_object(permanent_delete)

        self.ensure_property("id").after_execute(lambda _: _delete_object())
        return self

    @property
    def fun_settings(self) -> TeamFunSettings:
        """Settings to configure use of Giphy, memes, and stickers in the team."""
        return self.properties.get("funSettings", TeamFunSettings())

    @property
    def member_settings(self) -> TeamMemberSettings:
        """Settings to configure whether members can perform certain actions, for example,
        create channels and add bots, in the team."""
        return self.properties.get("memberSettings", TeamMemberSettings())

    @property
    def guest_settings(self) -> TeamGuestSettings:
        """Settings to configure whether guests can create, update, or delete channels in the team."""
        return self.properties.get("guestSettings", TeamGuestSettings())

    @property
    def messaging_settings(self) -> TeamMessagingSettings:
        """Settings to configure messaging and mentions in the team."""
        return self.properties.get("guestSettings", TeamMessagingSettings())

    @property
    def display_name(self) -> Optional[str]:
        """The name of the team."""
        return self.properties.get("displayName", None)

    @property
    def description(self) -> Optional[str]:
        """An optional description for the team."""
        return self.properties.get("description", None)

    @property
    def classification(self) -> Optional[str]:
        """An optional label. Typically describes the data or business sensitivity of the team.
        Must match one of a pre-configured set in the tenant's directory.
        """
        return self.properties.get("classification", None)

    @property
    def is_archived(self) -> Optional[bool]:
        """Whether this team is in read-only mode."""
        return self.properties.get("isArchived", None)

    @property
    def visibility(self) -> Optional[TeamVisibilityType]:
        """The visibility of the group and team. Defaults to Public."""
        return self.properties.get("visibility", TeamVisibilityType.unknown)

    @property
    def web_url(self) -> Optional[str]:
        """A hyperlink that will go to the team in the Microsoft Teams client. This is the URL that you get when
        you right-click a team in the Microsoft Teams client and select Get link to team. This URL should be treated
        as an opaque blob, and not parsed."""
        return self.properties.get("webUrl", None)

    @property
    def created_datetime(self):
        """Timestamp at which the team was created."""
        return self.properties.get("createdDateTime", None)

    @odata(name="allChannels")
    @property
    def all_channels(self) -> ChannelCollection:
        """
        List of channels either hosted in or shared with the team (incoming channels).
        """
        return self.properties.get(
            "allChannels", ChannelCollection(self.context, ResourcePath("allChannels", self.resource_path))
        )

    @odata(name="incomingChannels")
    @property
    def incoming_channels(self) -> ChannelCollection:
        """List of channels shared with the team."""
        return self.properties.get(
            "incomingChannels", ChannelCollection(self.context, ResourcePath("incomingChannels", self.resource_path))
        )

    @property
    def channels(self) -> ChannelCollection:
        """The collection of channels & messages associated with the team."""
        return self.properties.get(
            "channels", ChannelCollection(self.context, ResourcePath("channels", self.resource_path))
        )

    @property
    def group(self):
        """"""
        from office365.directory.groups.group import Group

        return self.properties.get("group", Group(self.context, ResourcePath("group", self.resource_path)))

    @odata(name="primaryChannel")
    @property
    def primary_channel(self) -> Channel:
        """The general channel for the team."""
        return self.properties.get(
            "primaryChannel", Channel(self.context, ResourcePath("primaryChannel", self.resource_path))
        )

    @property
    def schedule(self) -> Schedule:
        """The schedule of shifts for this team."""
        return self.properties.get("schedule", Schedule(self.context, ResourcePath("schedule", self.resource_path)))

    @odata(name="installedApps")
    @property
    def installed_apps(self) -> EntityCollection[TeamsAppInstallation]:
        """The apps installed in this team."""
        return self.properties.get(
            "installedApps",
            EntityCollection(self.context, TeamsAppInstallation, ResourcePath("installedApps", self.resource_path)),
        )

    @property
    def operations(self) -> EntityCollection[TeamsAsyncOperation]:
        """The async operations that ran or are running on this team."""
        return self.properties.setdefault(
            "operations",
            EntityCollection(self.context, TeamsAsyncOperation, ResourcePath("operations", self.resource_path)),
        )

    @odata(name="permissionGrants")
    @property
    def permission_grants(self) -> EntityCollection[ResourceSpecificPermissionGrant]:
        """
        List all resource-specific permission grants
        """
        return self.properties.setdefault(
            "permissionGrants",
            EntityCollection(self.context, ResourceSpecificPermissionGrant, ResourcePath("permissionGrants")),
        )

    @property
    def summary(self) -> TeamSummary:
        """Contains summary information about the team, including number of owners, members, and guests."""
        return self.properties.get("summary", TeamSummary())

    @property
    def tenant_id(self) -> Optional[str]:
        """The ID of the Azure Active Directory tenant."""
        return self.properties.get("tenantId", None)

    @property
    def tags(self) -> EntityCollection[TeamworkTag]:
        """The tags associated with the team."""
        return self.properties.get(
            "tags", EntityCollection(self.context, TeamworkTag, ResourcePath("tags", self.resource_path))
        )

    @property
    def template(self) -> TeamsTemplate:
        """The template this team was created from"""
        return self.properties.get("template", TeamsTemplate(self.context, ResourcePath("template", self.resource_path)))

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def first_channel_name(self) -> Optional[str]:
        """Gets the firstChannelName property"""
        return self.properties.get("firstChannelName", None)

    @property
    def internal_id(self) -> Optional[str]:
        """Gets the internalId property"""
        return self.properties.get("internalId", None)

    @property
    def specialization(self) -> TeamSpecialization:
        """Gets the specialization property"""
        return self.properties.get("specialization", TeamSpecialization.none)

    @property
    def members(self) -> ConversationMemberCollection:
        """Gets the members property"""
        return self.properties.get(
            "members",
            ConversationMemberCollection(self.context, ResourcePath("members", self.resource_path)),
        )

    @property
    def photo(self) -> ProfilePhoto:
        """Gets the photo property"""
        return self.properties.get("photo", ProfilePhoto(self.context, ResourcePath("photo", self.resource_path)))

    def archive(self) -> Self:
        """Archive the specified team. When a team is archived, users can no longer send or like messages on any
        channel in the team, edit the team's name, description, or other settings, or in general make most changes to
        the team. Membership changes to the team continue to be allowed."""
        qry = ServiceOperationQuery(self, "archive")
        self.context.add_query(qry)
        return self

    def unarchive(self) -> Self:
        """Restore an archived team. This restores users' ability to send messages and edit the team, abiding by
        tenant and team settings."""
        qry = ServiceOperationQuery(self, "unarchive")
        self.context.add_query(qry)
        return self

    def clone(self) -> Self:
        """Create a copy of a team. This operation also creates a copy of the corresponding group."""
        qry = ServiceOperationQuery(self, "clone")
        self.context.add_query(qry)
        return self

    def send_activity_notification(
        self,
        topic: TeamworkActivityTopic,
        activity_type: str,
        chain_id: str,
        preview_text: str,
        template_parameters: Dict[str, Any],
        recipient: TeamworkNotificationRecipient,
    ):
        """Send an activity feed notification in the scope of a team.
        For more details about sending notifications and the requirements for doing so,
        see sending Teams activity notifications:
        https://docs.microsoft.com/en-us/graph/teams-send-activityfeednotifications

        Args:
            topic (teamworkActivityTopic): Topic of the notification. Specifies the resource being talked about.
            activity_type (str): Activity type. This must be declared in the Teams app manifest.
            chain_id (str): Optional. Used to override a previous notification. Use the same chainId in subsequent requests to override the previous notification.
            preview_text (str): Preview text for the notification. Microsoft Teams will only show first 150 characters
            template_parameters (dict): Values for template variables defined in the activity feed entry corresponding to activityType in Teams app manifest.
            template_parameters (dict): Recipient of the notification. Only Azure AD users are supported.
            recipient (teamworkNotificationRecipient): Recipient of the notification
        """
        payload = {
            "topic": topic,
            "activityType": activity_type,
            "chainId": chain_id,
            "previewText": preview_text,
            "templateParameters": template_parameters,
            "recipient": recipient,
        }
        qry = ServiceOperationQuery(self, "sendActivityNotification", None, payload)
        self.context.add_query(qry)
        return self

    def set_property(self, name, value, persist_changes=True):
        super().set_property(name, value, persist_changes)
        if name == "id":
            if self._resource_path.segment == "team":
                self._resource_path = ResourcePath(value, ResourcePath("teams"))
        return self

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Team"
