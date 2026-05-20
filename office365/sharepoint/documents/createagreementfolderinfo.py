from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CreateAgreementFolderInfo(ClientValue):
    agreement_folder_server_relative_url: Optional[str] = None
    agreement_number: Optional[str] = None
