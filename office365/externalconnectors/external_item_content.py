from __future__ import annotations

from office365.externalconnectors.itemcontenttype import (
    ExternalItemContentType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ExternalItemContent(ClientValue):
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ExternalItemContent"

    type: ExternalItemContentType = ExternalItemContentType.text
