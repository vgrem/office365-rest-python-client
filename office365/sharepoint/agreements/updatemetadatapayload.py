from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UpdateAgreementMetaDataPayload(ClientValue):
    file_url: Optional[str] = None
    mark_as_termination_letter: Optional[bool] = None
