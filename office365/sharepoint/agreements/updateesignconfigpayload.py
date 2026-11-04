from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class UpdateAgreementESignConfigPayload(ClientValue):
    AgreementId: str | None = None
    AgreementUrl: str | None = None
    DocumentId: str | None = None
    eSignStatus: str | None = None
    MoveStateToInESign: bool | None = None
    RequestorEmail: str | None = None
    SignersEmail: StringCollection = field(default_factory=StringCollection)
