from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamsTabConfiguration(ClientValue):
    """The settings that determine the content of a tab.
    When a tab is interactively configured, this information is set by the tab provider application.
    In addition to the properties below, some tab provider applications specify additional custom properties.

    :param str content_url: Url used for rendering tab contents in Teams.
    :param str entity_id: Identifier for the entity hosted by the tab provider.
    :param str remove_url: Url called by Teams client when a Tab is removed using the Teams Client.
    :param str website_url: Url for showing tab contents outside of Teams.
    """

    contentUrl: str | None = None
    entityId: str | None = None
    removeUrl: str | None = None
    websiteUrl: str | None = None
