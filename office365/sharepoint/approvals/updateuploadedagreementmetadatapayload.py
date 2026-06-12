from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class UpdateUploadedAgreementMetadataPayload(ClientValue):
    AgreementNumber: str | None = None
    AgreementUrl: str | None = None
    Category: str | None = None
    Country: str | None = None
    IsDraft: bool | None = None
    IsExistingAgreement: bool | None = None
    Language: str | None = None
    State: str | None = None
