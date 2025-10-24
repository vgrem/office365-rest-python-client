from office365.runtime.client_value import ClientValue


class CloudPcAuditProperty(ClientValue):

    def __init__(self, display_name: str = None, new_value: str = None, old_value: str = None):
        self.displayName = display_name
        self.newValue = new_value
        self.oldValue = old_value

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcAuditProperty"
