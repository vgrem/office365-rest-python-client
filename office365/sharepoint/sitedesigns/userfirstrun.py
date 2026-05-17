from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.entity import Entity


class UserFirstRun(Entity):
    @property
    def experiences(self) -> ClientValueCollection[int]:
        """Gets the Experiences property"""
        return self.properties.get("Experiences", ClientValueCollection(int))
