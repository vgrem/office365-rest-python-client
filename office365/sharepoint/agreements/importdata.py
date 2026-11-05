from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AgreementImportData(ClientValue):
    ExtractionPending: int | None = None
    UserConfirmationPending: int | None = None
