from office365.runtime.client_value import ClientValue


class PortalLaunchSetupWrapper(ClientValue):

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalLaunch.PortalLaunchSetupWrapper"
