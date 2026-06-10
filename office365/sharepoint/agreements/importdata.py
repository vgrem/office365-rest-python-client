from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementImportData(ClientValue):
    ExtractionPending: int | None = None
    UserConfirmationPending: int | None = None
