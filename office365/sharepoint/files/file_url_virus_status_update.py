from __future__ import annotations

from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class FileUrlVirusStatusUpdate(Entity):
    @odata(name="fileUrl", beta=True)
    @property
    def file_url(self) -> Optional[str]:
        """Gets the fileUrl property"""
        return self.properties.get("fileUrl", None)

    @odata(name="virusMessage", beta=True)
    @property
    def virus_message(self) -> Optional[str]:
        """Gets the virusMessage property"""
        return self.properties.get("virusMessage", None)

    @odata(name="virusStatus", beta=True)
    @property
    def virus_status(self) -> bytes | None:
        """Gets the virusStatus property"""
        return self.properties.get("virusStatus", None)

    def update_virus_status(self) -> Self:
        """UpdateVirusStatus operation."""
        qry = ServiceOperationQuery(self, "UpdateVirusStatus", None, {}, None, None)
        self.context.add_query(qry)
        return self
