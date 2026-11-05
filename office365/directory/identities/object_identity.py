from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ObjectIdentity(ClientValue):
    """
    Represents an identity used to sign in to a user account.
    """

    signInType: str | None = None
    issuer: str | None = None
    issuerAssignedId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ObjectIdentity"
