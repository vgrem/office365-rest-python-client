from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class VivaConnectionsLicense(ClientValue):
    is_tenant_enabled: Optional[bool] = None
    is_user_enabled: Optional[bool] = None
