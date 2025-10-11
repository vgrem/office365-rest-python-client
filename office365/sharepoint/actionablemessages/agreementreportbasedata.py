from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.actionablemessages.agreementdatapair import AgreementDataPair


class AgreementReportBaseData(ClientValue):

    def __init__(
        self,
        by_expiration_status: ClientValueCollection[AgreementDataPair] = ClientValueCollection(AgreementDataPair),
        error_message: str = None,
        expired: int = None,
        in_effect: int = None,
        in_progress_by_state: ClientValueCollection[AgreementDataPair] = ClientValueCollection(AgreementDataPair),
        near_expiration: int = None,
    ):
        self.by_expiration_status = by_expiration_status
        self.error_message = error_message
        self.expired = expired
        self.in_effect = in_effect
        self.in_progress_by_state = in_progress_by_state
        self.near_expiration = near_expiration
