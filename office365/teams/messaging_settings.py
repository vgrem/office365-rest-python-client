from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamMessagingSettings(ClientValue):
    """Settings to configure messaging and mentions in the team.

    Args:
        allow_user_edit_messages (bool): If set to true, users can edit their messages.
        allow_user_delete_messages (bool): If set to true, users can delete their messages.
        allow_owner_delete_messages (bool): If set to true, owners can delete their messages.
        allow_team_mentions (bool): If set to true, owners can delete their messages.
        allow_channel_mentions (bool): If set to true, owners can delete their messages.
    """

    allowUserEditMessages: bool = True
    allowUserDeleteMessages: bool = True
    allowOwnerDeleteMessages: bool = True
    allowTeamMentions: bool = True
    allowChannelMentions: bool = True

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamMessagingSettings"
