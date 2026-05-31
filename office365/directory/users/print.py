from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath

class UserPrint(ClientValue):
    recentPrinterShares: EntityCollection[PrinterShare] | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.UserPrint'