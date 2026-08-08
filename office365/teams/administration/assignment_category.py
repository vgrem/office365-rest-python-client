from office365.runtime.client_value import ClientValue


class AssignmentCategory(ClientValue):
    primary = "0"
    private = "1"
    alternate = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.AssignmentCategory"
