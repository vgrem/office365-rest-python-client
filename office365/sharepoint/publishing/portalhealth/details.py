from office365.runtime.client_value import ClientValue


class PortalHealthDetails(ClientValue):
    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalHealthStatusDetails"
