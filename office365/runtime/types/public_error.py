from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.operations.public_error_detail import PublicErrorDetail
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.public_inner_error import PublicInnerError


@dataclass
class PublicError(ClientValue):
    code: str | None = None
    details: ClientValueCollection[PublicErrorDetail] = field(
        default_factory=lambda: ClientValueCollection(PublicErrorDetail)
    )
    innerError: PublicInnerError = field(default_factory=PublicInnerError)
    message: str | None = None
    target: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PublicError"
