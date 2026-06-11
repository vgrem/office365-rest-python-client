from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class GetNextAgreementWorkFlowRequest(ClientValue):
    CurrentState: int | None = None
    DocumentUri: str | None = None
