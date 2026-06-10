from __future__ import annotations

from office365.sharepoint.clientsidecomponent.card_element import CardElement


class AdaptiveCardImage(CardElement):
    backgroundColor: str | None = None
    height: str | None = None
    horizontalAlignment: str | None = None
    size: str | None = None
    style: str | None = None
    url: str | None = None
    width: str | None = None
    altText: str | None = None
