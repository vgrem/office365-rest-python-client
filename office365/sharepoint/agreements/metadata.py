from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.document import AgreementDocument


@dataclass
class AgreementMetaData(ClientValue):
    AgreementNumber: str | None = None
    Category: str | None = None
    Country: str | None = None
    CreatedBy: str | None = None
    CreatedTime: str | None = None
    Documents: ClientValueCollection[AgreementDocument] = field(
        default_factory=lambda: ClientValueCollection(AgreementDocument)
    )
    EndDate: str | None = None
    FirstParty: str | None = None
    Language: str | None = None
    Name: str | None = None
    Owner: str | None = None
    SecondParty: str | None = None
    SiteId: str | None = None
    StartDate: str | None = None
    State: str | None = None
    TotalValue: str | None = None
    Url: str | None = None
    WebId: str | None = None
    WebUrl: str | None = None
