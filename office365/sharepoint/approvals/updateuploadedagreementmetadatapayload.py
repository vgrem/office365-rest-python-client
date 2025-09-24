from office365.runtime.client_value import ClientValue


class UpdateUploadedAgreementMetadataPayload(ClientValue):

    def __init__(
        self,
        agreement_number: str = None,
        agreement_url: str = None,
        category: str = None,
        country: str = None,
        is_draft: bool = None,
        is_existing_agreement: bool = None,
        language: str = None,
        state: str = None,
    ):
        self.agreement_number = agreement_number
        self.agreement_url = agreement_url
        self.category = category
        self.country = country
        self.is_draft = is_draft
        self.is_existing_agreement = is_existing_agreement
        self.language = language
        self.state = state
