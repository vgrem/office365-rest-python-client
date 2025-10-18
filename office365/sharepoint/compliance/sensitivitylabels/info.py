from office365.runtime.client_value import ClientValue


class SensitivityLabelInfo(ClientValue):

    def __init__(self, display_name: str = None, id_: str = None, members_can_share: str = None):
        self.display_name = display_name
        self.id = id_
        self.members_can_share = members_can_share
