from typing import Optional

from office365.runtime.client_value import ClientValue


class MicrofeedUserPosts(ClientValue):
    def __init__(self, account_name: Optional[str] = None):
        self.AccountName = account_name

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedUserPosts"
