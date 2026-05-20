from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.document import AgreementDocument


@dataclass
class AgreementDocumentsInfo(ClientValue):
    documents: Optional[ClientValueCollection[AgreementDocument]] = None
