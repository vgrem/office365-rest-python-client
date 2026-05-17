from typing import Optional

from office365.runtime.client_value import ClientValue


class ConfiguredUserInfo(ClientValue):
    def __init__(
        self,
        email: Optional[str] = None,
        login_name: Optional[str] = None,
        name: Optional[str] = None,
        profile_pic_url: Optional[str] = None,
        user_id: Optional[int] = None,
    ):
        self.email = email
        self.login_name = login_name
        self.name = name
        self.profile_pic_url = profile_pic_url
        self.user_id = user_id
