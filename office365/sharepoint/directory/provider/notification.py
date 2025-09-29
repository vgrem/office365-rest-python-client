from typing_extensions import Self

from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.directory.provider.object_changes import (
    DirectoryObjectChanges,
)
from office365.sharepoint.entity import Entity


class DirectoryNotification(Entity):
    """"""

    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = StaticPath("SP.Directory.Provider.DirectoryNotification")
        super().__init__(context, resource_path)

    def notify_changes(self, directory_object_changes: DirectoryObjectChanges) -> Self:
        """ """
        payload = {"directoryObjectChanges": directory_object_changes}
        qry = ServiceOperationQuery(self, "NotifyChanges", None, payload, None, None)
        self.context.add_query(qry)
        return self

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.DirectoryNotification"
