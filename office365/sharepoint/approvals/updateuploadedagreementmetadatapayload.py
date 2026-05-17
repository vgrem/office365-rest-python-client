from typing import Optional

from office365.runtime.client_value import ClientValue


class UpdateUploadedAgreementMetadataPayload(ClientValue):
    def __init__(
        self,
        agreement_number: Optional[str] = None,
        agreement_url: Optional[str] = None,
        category: Optional[str] = None,
        country: Optional[str] = None,
        is_draft: Optional[bool] = None,
        is_existing_agreement: Optional[bool] = None,
        language: Optional[str] = None,
        state: Optional[str] = None,
    ):
        self.agreement_number = agreement_number
        self.agreement_url = agreement_url
        self.category = category
        self.country = country
        self.is_draft = is_draft
        self.is_existing_agreement = is_existing_agreement
        self.language = language
        self.state = state
