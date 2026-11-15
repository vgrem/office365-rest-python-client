from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.public_error_detail import PublicErrorDetail


class PublicInnerError(ClientValue):
    code: str | None = None
    details: ClientValueCollection[PublicErrorDetail] = field(
        default_factory=lambda: ClientValueCollection(PublicErrorDetail)
    )
    message: str | None = None
    target: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PublicInnerError"
