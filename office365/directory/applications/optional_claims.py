from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.optional_claim import OptionalClaim
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class OptionalClaims(ClientValue):
    """An application can configure optional claims to be returned in each of three types of tokens
    (ID token, access token, SAML 2 token) it can receive from the security token service.
    An application can configure a different set of optional claims to be returned in each token type.
    The optionalClaims property of the application is an optionalClaims object."""

    accessToken: ClientValueCollection[OptionalClaim] = field(default_factory=lambda: ClientValueCollection(OptionalClaim))
    idToken: ClientValueCollection[OptionalClaim] = field(default_factory=lambda: ClientValueCollection(OptionalClaim))
    saml2Token: ClientValueCollection[OptionalClaim] = field(default_factory=lambda: ClientValueCollection(OptionalClaim))

    @property
    def entity_type_name(self):
        return "microsoft.graph.OptionalClaims"
