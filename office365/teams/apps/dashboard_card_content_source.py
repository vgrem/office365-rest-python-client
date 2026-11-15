from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.teams.apps.dashboard_card_bot_configuration import TeamsAppDashboardCardBotConfiguration
from office365.teams.apps.dashboard_card_source_type import TeamsAppDashboardCardSourceType


class TeamsAppDashboardCardContentSource(ClientValue):
    botConfiguration: TeamsAppDashboardCardBotConfiguration = field(
        default_factory=TeamsAppDashboardCardBotConfiguration
    )
    sourceType: TeamsAppDashboardCardSourceType = TeamsAppDashboardCardSourceType.bot

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppDashboardCardContentSource"
