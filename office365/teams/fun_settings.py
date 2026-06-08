from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamFunSettings(ClientValue):
    """Settings to configure use of Giphy, memes, and stickers in the team.

    Args:
        allow_custom_memes (bool): f set to true, enables users to include custom memes.
        allow_giphy (bool): If set to true, enables Giphy use.
        allow_stickers_and_memes (bool): If set to true, enables users to include stickers and memes.
        giphy_content_rating (str): Giphy content rating. Possible values are: moderate, strict.
    """

    allowCustomMemes: bool | None = None
    allowGiphy: bool | None = None
    allowStickersAndMemes: bool | None = None
    giphyContentRating: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamFunSettings"
