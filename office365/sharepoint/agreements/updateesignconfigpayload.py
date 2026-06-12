from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class UpdateAgreementESignConfigPayload(ClientValue):
    AgreementId: str | None = None
    AgreementUrl: str | None = None
    DocumentId: str | None = None
    eSignStatus: str | None = None
    MoveStateToInESign: bool | None = None
    RequestorEmail: str | None = None
    SignersEmail: StringCollection = field(default_factory=StringCollection)
