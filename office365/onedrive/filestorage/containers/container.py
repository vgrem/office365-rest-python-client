from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata


class FileStorageContainer(Entity):
    """Represents a location where multiple users or a group of users can store files and access them
    via an application. All file system objects in a fileStorageContainer are returned as driveItem resources.
    """

    def activate(self) -> Self:
        """Activate a fileStorageContainer object.

        A container created in inactive state must be activated within 24 hours,
        or it will be automatically deleted. Upon activation, the status property
        changes from inactive to active.
        """
        qry = ServiceOperationQuery(self, "activate")
        self.context.add_query(qry)
        return self

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> Optional[datetime]:
        """Date and time of the fileStorageContainer creation. Read-only."""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "graph.fileStorageContainer"
