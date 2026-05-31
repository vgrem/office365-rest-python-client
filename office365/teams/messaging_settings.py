from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamMessagingSettings(ClientValue):
    """Settings to configure messaging and mentions in the team.

    :param bool allow_user_edit_messages: If set to true, users can edit their messages.
    :param bool allow_user_delete_messages: If set to true, users can delete their messages.
    :param bool allow_owner_delete_messages: If set to true, owners can delete their messages.
    :param bool allow_team_mentions: If set to true, owners can delete their messages.
    :param bool allow_channel_mentions: If set to true, owners can delete their messages.
    """

    allowUserEditMessages: bool = True
    allowUserDeleteMessages: bool = True
    allowOwnerDeleteMessages: bool = True
    allowTeamMentions: bool = True
    allowChannelMentions: bool = True

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamMessagingSettings"
