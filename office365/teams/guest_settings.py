from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamGuestSettings(ClientValue):
    """Settings to configure whether guests can create, update, or delete channels in the team.

    :param bool allow_create_update_channels:
    :param bool allow_delete_channels:
    """

    allowCreateUpdateChannels: bool = True
    allowDeleteChannels: bool = True
