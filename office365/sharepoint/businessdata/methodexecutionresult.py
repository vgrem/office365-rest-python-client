from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.businessdata.entityfieldvaluedictionary import EntityFieldValueDictionary
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection


class MethodExecutionResult(Entity):

    @property
    def return_parameter_collection(self) -> EntityCollection[EntityFieldValueDictionary]:
        """Gets the ReturnParameterCollection property"""
        return self.properties.get(
            "ReturnParameterCollection",
            EntityCollection[EntityFieldValueDictionary](
                self.context, EntityFieldValueDictionary, ResourcePath("ReturnParameterCollection", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self):
        return "SP.BusinessData.MethodExecutionResult"
