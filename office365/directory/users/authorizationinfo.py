from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class AuthorizationInfo(ClientValue):
    def __init__(self, certificate_user_ids: StringCollection = StringCollection()):
        self.certificateUserIds = certificate_user_ids

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthorizationInfo"
