from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamFunSettings(ClientValue):
    """Settings to configure use of Giphy, memes, and stickers in the team.

    :param bool allow_custom_memes: f set to true, enables users to include custom memes.
    :param bool allow_giphy: If set to true, enables Giphy use.
    :param bool allow_stickers_and_memes: 	If set to true, enables users to include stickers and memes.
    :param str giphy_content_rating: Giphy content rating. Possible values are: moderate, strict.
    """

    allowCustomMemes: bool | None = None
    allowGiphy: bool | None = None
    allowStickersAndMemes: bool | None = None
    giphyContentRating: str | None = None
