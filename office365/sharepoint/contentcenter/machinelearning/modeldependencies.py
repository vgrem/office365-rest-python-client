from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.contentcenter.machinelearning.dependentmodel import (
    SPDependentModel,
)


@dataclass
class SPModelDependencies(ClientValue):
    DependentModels: Optional[ClientValueCollection[SPDependentModel]] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPModelDependencies"
