from typing import Optional

from office365.directory.invitations.message_info import InvitedUserMessageInfo
from office365.directory.objects.object import DirectoryObject
from office365.directory.users.user import User
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class Invitation(Entity):
    """Represents an invitation that is used to add external users to an organization.

    The invitation process uses the following flow:

      - An invitation is created
      - An invitation is sent to the invited user (containing an invitation link)
      - The invited user clicks on the invitation link, signs in and redeems the invitation and creation of the
        user entity representing the invited user completes
      - The user is redirected to a specific page after redemption completes

     Creating an invitation will return a redemption URL in the response (inviteRedeemUrl).
     The create invitation API can automatically send an email containing the redemption URL to the invited user,
     by setting the sendInvitationMessage to true. You can also customize the message that will be sent to
     the invited user. Instead, if you wish to send the redemption URL through some other means, you can set the
     sendInvitationMessage to false and use the redeem URL from the response to craft your own communication.
     Currently, there is no API to perform the redemption process. The invited user has to click on the inviteRedeemUrl
     link sent in the communication in the step above, and go through the interactive redemption process in a browser.
     Once completed, the invited user becomes an external user in the organization.
    """

    @property
    def invited_user_display_name(self) -> Optional[str]:
        """The display name of the user being invited."""
        return self.properties.get("invitedUserDisplayName", None)

    @property
    def invited_user_email_address(self) -> Optional[str]:
        """The email address of the user being invited."""
        return self.properties.get("invitedUserEmailAddress", None)

    @odata(name="invitedUserMessageInfo")
    @property
    def invited_user_message_info(self) -> InvitedUserMessageInfo:
        """"""
        return self.properties.get("invitedUserMessageInfo", InvitedUserMessageInfo())

    @odata(name="invitedUser")
    @property
    def invited_user(self) -> User:
        """The user created as part of the invitation creation."""
        return self.properties.get("invitedUser", User(self.context, ResourcePath("invitedUser", self.resource_path)))

    @property
    def invited_user_type(self) -> Optional[str]:
        """Gets the invitedUserType property"""
        return self.properties.get("invitedUserType", None)

    @property
    def invite_redeem_url(self) -> Optional[str]:
        """Gets the inviteRedeemUrl property"""
        return self.properties.get("inviteRedeemUrl", None)

    @property
    def invite_redirect_url(self) -> Optional[str]:
        """Gets the inviteRedirectUrl property"""
        return self.properties.get("inviteRedirectUrl", None)

    @property
    def reset_redemption(self) -> Optional[bool]:
        """Gets the resetRedemption property"""
        return self.properties.get("resetRedemption", None)

    @property
    def send_invitation_message(self) -> Optional[bool]:
        """Gets the sendInvitationMessage property"""
        return self.properties.get("sendInvitationMessage", None)

    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def invited_user_sponsors(self) -> EntityCollection[DirectoryObject]:
        """Gets the invitedUserSponsors property"""
        return self.properties.get(
            "invitedUserSponsors",
            EntityCollection[DirectoryObject](
                self.context, DirectoryObject, ResourcePath("invitedUserSponsors", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Invitation"
