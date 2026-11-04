from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UpdateUploadedAgreementMetadataPayload(ClientValue):
    AgreementNumber: str | None = None
    AgreementUrl: str | None = None
    Category: str | None = None
    Country: str | None = None
    IsDraft: bool | None = None
    IsExistingAgreement: bool | None = None
    Language: str | None = None
    State: str | None = None
