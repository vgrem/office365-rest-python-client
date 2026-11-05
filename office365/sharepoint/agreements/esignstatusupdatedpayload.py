from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class AgreementESignStatusUpdatedPayload(ClientValue):
    agreement_id: Optional[str] = None
    external_reference: Optional[str] = None
    signed_doc_id: Optional[str] = None
    status: Optional[str] = None
