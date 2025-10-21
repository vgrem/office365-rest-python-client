from office365.runtime.client_value import ClientValue


class ModifiedProperty(ClientValue):

    def __init__(self, name: str = None, new_value: str = None, old_value: str = None, display_name: str = None):
        self.Name = name
        self.NewValue = new_value
        self.OldValue = old_value
        self.displayName = display_name

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.ModifiedProperty"
