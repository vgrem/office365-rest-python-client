from office365.runtime.client_value import ClientValue


class ConfiguredUserInfo(ClientValue):
    def __init__(
        self,
        email: str = None,
        login_name: str = None,
        name: str = None,
        profile_pic_url: str = None,
        user_id: int = None,
    ):
        self.email = email
        self.login_name = login_name
        self.name = name
        self.profile_pic_url = profile_pic_url
        self.user_id = user_id
