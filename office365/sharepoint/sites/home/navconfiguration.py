from office365.runtime.client_value import ClientValue
from typing import Optional


class HomeSiteNavConfiguration(ClientValue):
    def __init__(self, is_enabled: Optional[bool] = None, logo_hash: Optional[str] = None):
        self.is_enabled = is_enabled
        self.logo_hash = logo_hash
