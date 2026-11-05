from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.contentcenter.machinelearning.dependentmodel import (
    SPDependentModel,
)


class SPModelDependencies(ClientValue):
    DependentModels: ClientValueCollection[SPDependentModel] = field(
        default_factory=lambda: ClientValueCollection(SPDependentModel)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPModelDependencies"
