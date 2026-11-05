from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class WacToken(ClientValue):
    AccessToken: Optional[str] = None
    AccessTokenTtl: Optional[int] = None
    AppUrl: Optional[str] = None
    ErrorMessageToDisplay: Optional[str] = None
    FavIconTarget: Optional[str] = None
    RedirectUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Yammer.WacToken"
