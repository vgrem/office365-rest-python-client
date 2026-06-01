from office365.directory.identitygovernance.accessreview.history.definition import AccessReviewHistoryDefinition
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AccessReviewSet(Entity):
    """
    Container for the base resources that expose the access reviews API and features. Currently exposes only the
    accessReviewScheduleDefinition relationship.
    """

    @odata(name="historyDefinitions")
    @property
    def history_definitions(self):
        """
        Represents a collection of access review history data and the scopes used to collect that data
        """
        return self.properties.get(
            "historyDefinitions",
            EntityCollection(
                self.context, AccessReviewHistoryDefinition, ResourcePath("historyDefinitions", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewSet"
