from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AppViewCreationInfo(ClientValue):
    app_id: Optional[str] = None
    is_private: Optional[bool] = None
    title: Optional[str] = None
