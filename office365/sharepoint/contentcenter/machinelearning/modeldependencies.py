from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.contentcenter.machinelearning.dependentmodel import (
    SPDependentModel,
)


class SPModelDependencies(ClientValue):

    def __init__(
        self, dependent_models: ClientValueCollection[SPDependentModel] = None
    ):
        self.DependentModels = dependent_models
