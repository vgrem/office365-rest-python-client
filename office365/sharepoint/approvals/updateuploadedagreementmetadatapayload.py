from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UpdateUploadedAgreementMetadataPayload(ClientValue):
    agreement_number: Optional[str] = None
    agreement_url: Optional[str] = None
    category: Optional[str] = None
    country: Optional[str] = None
    is_draft: Optional[bool] = None
    is_existing_agreement: Optional[bool] = None
    language: Optional[str] = None
    state: Optional[str] = None
