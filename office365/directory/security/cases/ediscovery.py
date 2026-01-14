from office365.directory.security.cases.operation import CaseOperation
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class EdiscoveryCase(Entity):
    """In the context of eDiscovery, contains custodians, searches, review sets. For details, see Overview of
    Microsoft Purview eDiscovery (Premium).
    """

    @property
    def operations(self):
        # type: () -> EntityCollection[CaseOperation]
        """Returns a list of case caseOperation objects for this case."""
        return self.properties.get(
            "operations",
            EntityCollection(
                self.context,
                CaseOperation,
                ResourcePath("operations", self.resource_path),
            ),
        )
