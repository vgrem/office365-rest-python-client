from office365.runtime.client_value import ClientValue


class CreateAgreementFolderInfo(ClientValue):
    def __init__(
        self,
        agreement_folder_server_relative_url: str = None,
        agreement_number: str = None,
    ):
        self.agreement_folder_server_relative_url = agreement_folder_server_relative_url
        self.agreement_number = agreement_number
