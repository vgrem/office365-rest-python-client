from __future__ import annotations

from office365.runtime.client_value import ClientValue


class GetNextAgreementWorkFlowRequest(ClientValue):
    CurrentState: int | None = None
    DocumentUri: str | None = None
