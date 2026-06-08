from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamsTabConfiguration(ClientValue):
    """The settings that determine the content of a tab.
    When a tab is interactively configured, this information is set by the tab provider application.
    In addition to the properties below, some tab provider applications specify additional custom properties.

    Args:
        content_url (str): Url used for rendering tab contents in Teams.
        entity_id (str): Identifier for the entity hosted by the tab provider.
        remove_url (str): Url called by Teams client when a Tab is removed using the Teams Client.
        website_url (str): Url for showing tab contents outside of Teams.
    """

    contentUrl: str | None = None
    entityId: str | None = None
    removeUrl: str | None = None
    websiteUrl: str | None = None
