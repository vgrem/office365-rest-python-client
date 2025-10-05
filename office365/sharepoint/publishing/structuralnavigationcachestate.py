from office365.runtime.client_value import ClientValue


class StructuralNavigationCacheState(ClientValue):

    def __init__(self, is_enabled: bool = None):
        self.IsEnabled = is_enabled

    @property
    def entity_type_name(self):
        return "SP.Publishing.Navigation.StructuralNavigationCacheState"
