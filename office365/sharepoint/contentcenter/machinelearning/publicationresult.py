from office365.runtime.client_value import ClientValue
from office365.sharepoint.contentcenter.machinelearning.publicationentitydata import (
    SPMachineLearningPublicationEntityData,
)


class SPMachineLearningPublicationResult(ClientValue):

    def __init__(
        self,
        error_message: str = None,
        publication: SPMachineLearningPublicationEntityData = SPMachineLearningPublicationEntityData(),
        status_code: int = None,
    ):
        self.ErrorMessage = error_message
        self.Publication = publication
        self.StatusCode = status_code

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningPublicationResult"
