from typing import Optional

from office365.runtime.client_value import ClientValue


class MicrofeedUserPosts(ClientValue):
    AccountName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedUserPosts"
