from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.document import AgreementDocument


class AgreementMetaData(ClientValue):
    def __init__(
        self,
        agreement_number: Optional[str] = None,
        category: Optional[str] = None,
        country: Optional[str] = None,
        created_by: Optional[str] = None,
        created_time: Optional[str] = None,
        documents: ClientValueCollection[AgreementDocument] = ClientValueCollection(AgreementDocument),
        end_date: Optional[str] = None,
        first_party: Optional[str] = None,
        language: Optional[str] = None,
        name: Optional[str] = None,
        owner: Optional[str] = None,
        second_party: Optional[str] = None,
        site_id: Optional[str] = None,
        start_date: Optional[str] = None,
        state: Optional[str] = None,
        total_value: Optional[str] = None,
        url: Optional[str] = None,
        web_id: Optional[str] = None,
        web_url: Optional[str] = None,
    ):
        self.agreement_number = agreement_number
        self.category = category
        self.country = country
        self.created_by = created_by
        self.created_time = created_time
        self.documents = documents
        self.end_date = end_date
        self.first_party = first_party
        self.language = language
        self.name = name
        self.owner = owner
        self.second_party = second_party
        self.site_id = site_id
        self.start_date = start_date
        self.state = state
        self.total_value = total_value
        self.url = url
        self.web_id = web_id
        self.web_url = web_url
