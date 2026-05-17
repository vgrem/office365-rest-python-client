from typing import Optional

from office365.runtime.client_value import ClientValue


class HomeSiteNavConfiguration(ClientValue):
    def __init__(self, is_enabled: Optional[bool] = None, logo_hash: Optional[str] = None):
        self.is_enabled = is_enabled
        self.logo_hash = logo_hash
