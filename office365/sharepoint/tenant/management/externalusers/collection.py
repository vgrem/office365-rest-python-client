from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.tenant.management.externalusers.external_user import (
    ExternalUser,
)


class ExternalUserCollection(EntityCollection[ExternalUser]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, ExternalUser, resource_path)

    def get_by_id(self, unique_id: str) -> ExternalUser:
        """Args:
            unique_id (str): The Id of the external user.
        """
        return ExternalUser(
            self.context,
            ServiceOperationPath("GetById", [unique_id], self.resource_path),
        )
