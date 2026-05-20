from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.document import AgreementDocument


@dataclass
class AgreementMetaData(ClientValue):
    agreement_number: Optional[str] = None
    category: Optional[str] = None
    country: Optional[str] = None
    created_by: Optional[str] = None
    created_time: Optional[str] = None
    documents: ClientValueCollection[AgreementDocument] = field(
        default_factory=lambda: ClientValueCollection(AgreementDocument)
    )
    end_date: Optional[str] = None
    first_party: Optional[str] = None
    language: Optional[str] = None
    name: Optional[str] = None
    owner: Optional[str] = None
    second_party: Optional[str] = None
    site_id: Optional[str] = None
    start_date: Optional[str] = None
    state: Optional[str] = None
    total_value: Optional[str] = None
    url: Optional[str] = None
    web_id: Optional[str] = None
    web_url: Optional[str] = None
