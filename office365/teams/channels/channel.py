from datetime import datetime
from typing import Optional
from urllib.parse import quote

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.teams.channels.membership_type import ChannelMembershipType
from office365.teams.channels.provision_email_result import ProvisionChannelEmailResult
from office365.teams.channels.shared_team_info import SharedWithChannelTeamInfo
from office365.teams.chats.messages.message import ChatMessage
from office365.teams.members.conversation import ConversationMember
from office365.teams.tabs.tab import TeamsTab


class Channel(Entity):
    """Teams are made up of channels, which are the conversations you have with your teammates"""

    def __str__(self):
        return self.display_name or self.entity_type_name

    def does_user_have_access(
        self,
        user_id: str = None,
        tenant_id: str = None,
        user_principal_name: str = None,
    ) -> ClientResult[bool]:
        """Determine whether a user has access to a shared channel.

        :param str user_id: Unique identifier for the user. Either specify the userId or the userPrincipalName property
           in the request.
        :param str tenant_id: The ID of the Azure Active Directory tenant that the user belongs to.
             The default value for this property is the current tenantId of the signed-in user or app.
        :param str user_principal_name: The user principal name (UPN) of the user. Either specify the userId or the
             userPrincipalName property in the request.
        """
        return_type = ClientResult(self.context)
        params = {
            "userId": user_id,
            "tenantId": tenant_id,
            "userPrincipalName": user_principal_name,
        }
        qry = FunctionQuery(self, "doesUserHaveAccess", params, return_type)
        self.context.add_query(qry)
        return return_type

    def provision_email(self) -> ClientResult[ProvisionChannelEmailResult]:
        """
        Provision an email address for a channel.

        Microsoft Teams doesn't automatically provision an email address for a channel by default.
        To have Teams provision an email address, you can call provisionEmail, or through the Teams user interface,
        select Get email address, which triggers Teams to generate an email address if it has not already provisioned
        one.

        To remove the email address of a channel, use the removeEmail method.
        """
        return_type = ClientResult(self.context, ProvisionChannelEmailResult())
        qry = ServiceOperationQuery(self, "provisionEmail", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def remove_email(self):
        """
        Remove the email address of a channel.
        You can remove an email address only if it was provisioned using the provisionEmail method or through
        the Microsoft Teams client.
        """
        qry = ServiceOperationQuery(self, "removeEmail")
        self.context.add_query(qry)
        return self

    @property
    def created_datetime(self) -> Optional[datetime]:
        """
        Read only. Timestamp at which the channel was created.
        """
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def description(self) -> Optional[str]:
        """Optional textual description for the channel."""
        return self.properties.get("Description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Channel name as it will appear to the user in Microsoft Teams. The maximum length is 50 characters"""
        return self.properties.get("displayName", None)

    @property
    def email(self) -> Optional[str]:
        """The email address for sending messages to the channel. Read-only."""
        return self.properties.get("email", None)

    @property
    def is_archived(self) -> Optional[bool]:
        """Indicates whether the channel is archived. Read-only."""
        return self.properties.get("isArchived", None)

    @property
    def is_favorite_by_default(self) -> Optional[bool]:
        """Indicates whether the channel should be marked as recommended for all members of the team to show in
        their channel list. Note: All recommended channels automatically show in the channels list for
        education and frontline worker users. The property can only be set programmatically via the Create team method.
        The default value is false"""
        return self.properties.get("isFavoriteByDefault", None)

    @property
    def tenant_id(self) -> Optional[str]:
        """The ID of the Microsoft Entra tenant."""
        return self.properties.get("tenantId", None)

    @property
    def membership_type(self) -> Optional[ChannelMembershipType]:
        """
        The type of the channel. Can be set during creation and can't be changed.
        The possible values are: standard, private, unknownFutureValue, shared. The default value is standard.
        Note that you must use the Prefer: include-unknown-enum-members request header to get the following value
        in this evolvable enum: shared.
        """
        return self.properties.get("membershipType", ChannelMembershipType.invalid)

    @property
    def web_url(self) -> Optional[str]:
        """A hyperlink that will navigate to the channel in Microsoft Teams. This is the URL that you get when you
        right-click a channel in Microsoft Teams and select Get link to channel. This URL should be treated as an
        opaque blob, and not parsed. Read-only."""
        return self.properties.get("webUrl", None)

    @property
    def files_folder(self) -> DriveItem:
        """Get the metadata for the location where the files of a channel are stored."""
        return self.properties.get(
            "filesFolder",
            DriveItem(self.context, ResourcePath("filesFolder", self.resource_path)),
        )

    @property
    def tabs(self) -> EntityCollection[TeamsTab]:
        """A collection of all the tabs in the channel. A navigation property."""
        return self.properties.get(
            "tabs",
            EntityCollection(self.context, TeamsTab, ResourcePath("tabs", self.resource_path)),
        )

    @property
    def messages(self) -> EntityCollection[ChatMessage]:
        """A collection of all the messages in the channel."""
        return self.properties.get(
            "messages",
            EntityCollection(self.context, ChatMessage, ResourcePath("messages", self.resource_path)),
        )

    @property
    def members(self) -> EntityCollection[ConversationMember]:
        """A collection of membership records associated with the channel."""
        return self.properties.get(
            "members",
            EntityCollection(
                self.context,
                ConversationMember,
                ResourcePath("members", self.resource_path),
            ),
        )

    @property
    def shared_with_teams(self) -> EntityCollection[SharedWithChannelTeamInfo]:
        """A collection of teams with which a channel is shared."""
        return self.properties.get(
            "sharedWithTeams",
            EntityCollection(
                self.context,
                SharedWithChannelTeamInfo,
                ResourcePath("sharedWithTeams", self.resource_path),
            ),
        )

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "createdDateTime": self.created_datetime,
                "filesFolder": self.files_folder,
                "sharedWithTeams": self.shared_with_teams,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)

    def set_property(self, name, value, persist_changes=True):
        super().set_property(name, value, persist_changes)
        # fallback: fix resource path
        if name == "id":
            self._resource_path = ResourcePath(quote(value), self.resource_path.parent)
        return self
