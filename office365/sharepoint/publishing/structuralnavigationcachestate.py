from typing import Optional

from office365.runtime.client_value import ClientValue


class StructuralNavigationCacheState(ClientValue):
    IsEnabled: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.Navigation.StructuralNavigationCacheState"
