from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ConfiguredUserInfo(ClientValue):
    email: Optional[str] = None
    login_name: Optional[str] = None
    name: Optional[str] = None
    profile_pic_url: Optional[str] = None
    user_id: Optional[int] = None
