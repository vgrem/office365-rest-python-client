from __future__ import annotations

from office365.outlook.resource_link_type import ResourceLinkType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ResourceLink(ClientValue):
    linkType: ResourceLinkType = ResourceLinkType.url
    name: str | None = None
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResourceLink"
