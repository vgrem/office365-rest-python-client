"""What a token proves, read without trusting it.

A requirement is usually answered from the tenant's grants, which says what the *tenant*
allowed. A token says what the *identity holding it* may do, which is the question a caller
about to send a request actually has - and it is the only answer available to a program that
holds a token but may not read directory grants, such as a SharePoint-only client that has no
Graph token at all.

Reading it is cheap: the payload of a JWT is base64url JSON. The signature is deliberately not
checked - this answers "what did the identity provider put in the token I hold", not "is this
token genuine". A token this process obtained came over TLS from the provider; one handed in
from outside has already been validated, or not, by whoever accepted it.

This module is pure: it holds no client and sends no request.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from office365.azure_env import AzureEnvironment, get_graph_authority
from office365.directory.applications.app_ids import MsAppIds
from office365.permissions.resource import ResourceName

if TYPE_CHECKING:
    from office365.permissions.requirement import Requirement

#: The ``aud`` an API's access token names: a URI for the cloud-hosted services, the API's own
#: application id for SharePoint and Exchange. An API that is not listed cannot be checked from
#: a token (the reader answers "unverifiable" rather than guessing), which is why this is a table
#: rather than a rule.
_AUDIENCES: dict[str, tuple[str, ...]] = {
    ResourceName.Graph: tuple(get_graph_authority(environment) for environment in AzureEnvironment),
    ResourceName.SharePoint: (MsAppIds.Office_365_SharePoint_Online,),
    ResourceName.Exchange: (MsAppIds.Office_365_Exchange_Online,),
    # Resource Manager's global audience; the sovereign clouds serve their own host
    ResourceName.Azure: ("https://management.core.windows.net",),
}


@dataclass(frozen=True)
class TokenClaims:
    """The claims of one access token that a permission check reads.

    ``delegated`` is ``None`` when the token carries no ``scp`` claim, and ``application`` is
    ``None`` when it carries no ``roles`` claim. A user's token has scopes and no roles, an
    app-only token the other way round, and the absence is what tells "this flow does not apply"
    apart from "this flow grants nothing".
    """

    audience: str
    delegated: frozenset[str] | None = None
    application: frozenset[str] | None = None

    @classmethod
    def parse(cls, token: str | None) -> TokenClaims | None:
        """The claims of ``token``, or ``None`` when there is no readable JWT to read."""
        payload = _payload(token)
        if payload is None:
            return None
        scopes = payload.get("scp")
        roles = payload.get("roles")
        return cls(
            audience=str(payload.get("aud") or ""),
            delegated=None if scopes is None else frozenset(str(scopes).split()),
            application=None if roles is None else frozenset(str(role) for role in roles),
        )

    def proves(self, requirement: Requirement) -> frozenset[str] | None:
        """The names this token proves for ``requirement``, or ``None`` if it cannot say.

        ``None`` sends the caller back to the tenant's grants, and covers both ways a token can
        be silent: it was issued for another API (a name is only a grant on the API that defines
        it) or for the other flow (a requirement that names application permissions is not
        answered by a user's ``scp``).
        """
        if self.audience.partition("@")[0] not in _AUDIENCES.get(str(requirement.resource), ()):
            return None
        if requirement.application:
            return self.application
        if requirement.delegated:
            return self.delegated
        return frozenset()


def _payload(token: str | None) -> dict[str, Any] | None:
    """The decoded payload of a JWT, or ``None`` for anything that is not one.

    An opaque token (no ``.``-separated parts), a payload that is not JSON and a payload that is
    not an object all answer ``None``: none of them is evidence about a permission.
    """
    header, _, rest = (token or "").partition(".")
    body, _, signature = rest.rpartition(".")
    if not header or not body or not signature:
        return None
    try:
        decoded = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    except ValueError:  # includes binascii.Error and json.JSONDecodeError
        return None
    return decoded if isinstance(decoded, dict) else None
