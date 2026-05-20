from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.contentcenter.machinelearning.publicationentitydata import (
    SPMachineLearningPublicationEntityData,
)


@dataclass
class SPMachineLearningPublicationResult(ClientValue):
    ErrorMessage: Optional[str] = None
    Publication: SPMachineLearningPublicationEntityData = field(default_factory=SPMachineLearningPublicationEntityData)
    StatusCode: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningPublicationResult"
