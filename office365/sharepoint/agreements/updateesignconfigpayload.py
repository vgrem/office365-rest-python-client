from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class UpdateAgreementESignConfigPayload(ClientValue):
    agreement_id: Optional[str] = None
    agreement_url: Optional[str] = None
    document_id: Optional[str] = None
    e_sign_status: Optional[str] = None
    move_state_to_in_e_sign: Optional[bool] = None
    requestor_email: Optional[str] = None
    signers_email: StringCollection = field(default_factory=StringCollection)
