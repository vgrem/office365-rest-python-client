from office365.directory.authentication.methods.modes import AuthenticationMethodModes
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


class UpdateAllowedCombinationsResult(ClientValue):

    def __init__(
        self,
        additional_information: str = None,
        conditional_access_references: StringCollection = StringCollection(),
        current_combinations: ClientValueCollection[AuthenticationMethodModes] = ClientValueCollection(
            AuthenticationMethodModes
        ),
        previous_combinations: ClientValueCollection[AuthenticationMethodModes] = ClientValueCollection(
            AuthenticationMethodModes
        ),
    ):
        self.additionalInformation = additional_information
        self.conditionalAccessReferences = conditional_access_references
        self.currentCombinations = current_combinations
        self.previousCombinations = previous_combinations

    " "

    @property
    def entity_type_name(self):
        return "microsoft.graph.UpdateAllowedCombinationsResult"
