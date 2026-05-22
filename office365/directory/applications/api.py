from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.preauthorized import PreAuthorizedApplication
from office365.directory.permissions.scope import PermissionScope
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


@dataclass
class ApiApplication(ClientValue):
    """Specifies settings for an application that implements a web API."""

    acceptMappedClaims: bool | None = None
    knownClientApplications: StringCollection = field(default_factory=StringCollection)
    oauth2PermissionScopes: ClientValueCollection[PermissionScope] = field(
        default_factory=lambda: ClientValueCollection(PermissionScope)
    )
    preAuthorizedApplications: ClientValueCollection[PreAuthorizedApplication] = field(
        default_factory=lambda: ClientValueCollection(PreAuthorizedApplication)
    )
    requestedAccessTokenVersion: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ApiApplication"
