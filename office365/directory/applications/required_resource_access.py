from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.resource_access import ResourceAccess
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class RequiredResourceAccess(ClientValue):
    """Specifies the set of OAuth 2.0 permission scopes and app roles under the specified resource that an
    application requires access to. The application may request the specified OAuth 2.0 permission scopes or app
    roles through the requiredResourceAccess property, which is a collection of requiredResourceAccess objects.
    """

    resourceAccess: ClientValueCollection[ResourceAccess] = field(
        default_factory=lambda: ClientValueCollection(ResourceAccess)
    )
    resourceAppId: str | None = None

    def __repr__(self):
        return self.resourceAppId or self.entity_type_name

    @property
    def entity_type_name(self):
        return "microsoft.graph.RequiredResourceAccess"
