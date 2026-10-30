"""The team settings getters read their own member, not a neighbour's.

``Team.messaging_settings`` read ``guestSettings`` and answered a fresh
``TeamMessagingSettings`` whatever the payload carried, so a caller reading the
messaging settings of a team that had them was handed an empty object -- and writing
them back sent the guest settings under the wrong name.
"""

from __future__ import annotations

from office365.migration.offline import offline_context
from office365.teams.messaging_settings import TeamMessagingSettings
from office365.teams.team import Team


def test_the_messaging_settings_getter_reads_the_messaging_member() -> None:
    team = Team(offline_context())
    messaging = TeamMessagingSettings()
    team.set_property("messagingSettings", messaging)

    assert team.messaging_settings is messaging
