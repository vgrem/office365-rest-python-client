from typing import Optional

from office365.runtime.client_value import ClientValue


class CreateAgreementFolderInfo(ClientValue):
    def __init__(
        self, agreement_folder_server_relative_url: Optional[str] = None, agreement_number: Optional[str] = None
    ):
        self.agreement_folder_server_relative_url = agreement_folder_server_relative_url
        self.agreement_number = agreement_number
