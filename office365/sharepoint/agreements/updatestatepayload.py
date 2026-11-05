from __future__ import annotations

from office365.runtime.client_value import ClientValue


class UpdateAgreementStatePayload(ClientValue):
    AgreementUrl: str | None = None
    CurrentState: int | None = None
    NextState: int | None = None
