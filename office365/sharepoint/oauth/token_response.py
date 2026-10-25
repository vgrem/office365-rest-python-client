from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.sharepoint.oauth.accesstokenoptionalclaim import (
        AccessTokenOptionalClaim,
    )


class TokenResponse(Entity):
    """ """

    @odata(name="access_token")
    @property
    def access_token(self) -> Optional[str]:
        """Gets the access_token property"""
        return self.properties.get("access_token", None)

    @odata(name="expires_on")
    @property
    def expires_on(self) -> Optional[str]:
        """Gets the expires_on property"""
        return self.properties.get("expires_on", None)

    @odata(name="id_token")
    @property
    def id_token(self) -> Optional[str]:
        """Gets the id_token property"""
        return self.properties.get("id_token", None)

    @odata(name="resource")
    @property
    def resource(self) -> Optional[str]:
        """Gets the resource property"""
        return self.properties.get("resource", None)

    @odata(name="scope")
    @property
    def scope(self) -> Optional[str]:
        """Gets the scope property"""
        return self.properties.get("scope", None)

    @odata(name="token_type")
    @property
    def token_type(self) -> Optional[str]:
        """Gets the token_type property"""
        return self.properties.get("token_type", None)

    @odata(name="accessTokenOptionalClaim", navigation=True)
    @property
    def access_token_optional_claim(self) -> AccessTokenOptionalClaim:
        """Gets the accessTokenOptionalClaim property"""
        from office365.sharepoint.oauth.accesstokenoptionalclaim import (
            AccessTokenOptionalClaim,
        )

        return self.properties.get(
            "accessTokenOptionalClaim",
            AccessTokenOptionalClaim(self.context, ResourcePath("accessTokenOptionalClaim", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "SP.OAuth.TokenResponse"
