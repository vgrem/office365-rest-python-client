from office365.runtime.client_value import ClientValue


class AddressBarLinkSettings(ClientValue):
    def __init__(self, link_disabled: bool = None, link_permission: int = None):
        self.linkDisabled = link_disabled
        self.linkPermission = link_permission

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.AddressBarLinkSettings"
