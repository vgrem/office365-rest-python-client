from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.document import AgreementDocument


class AgreementMetaData(ClientValue):
    def __init__(
        self,
        agreement_number: str = None,
        category: str = None,
        country: str = None,
        created_by: str = None,
        created_time: str = None,
        documents: ClientValueCollection[AgreementDocument] = ClientValueCollection(AgreementDocument),
        end_date: str = None,
        first_party: str = None,
        language: str = None,
        name: str = None,
        owner: str = None,
        second_party: str = None,
        site_id: str = None,
        start_date: str = None,
        state: str = None,
        total_value: str = None,
        url: str = None,
        web_id: str = None,
        web_url: str = None,
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
