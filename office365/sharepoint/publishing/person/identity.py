from office365.runtime.client_value import ClientValue


class PersonIdentity(ClientValue):

    def __init__(
        self, aad_object_id: str = None, display_name: str = None, user_name: str = None
    ):
        self.AadObjectId = aad_object_id
        self.DisplayName = display_name
        self.UserName = user_name
