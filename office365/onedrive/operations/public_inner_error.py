from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.operations.public_error_detail import PublicErrorDetail
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
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
