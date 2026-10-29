from __future__ import annotations

from typing import Optional

from office365.common.mail_folder_operation_status import MailFolderOperationStatus
from office365.entity import Entity
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata, version


@version("beta")
class MailFolderOperation(PollableOperation, Entity):
    @odata(name="resourceLocation")
    @property
    def resource_location(self) -> Optional[str]:
        """Gets the resourceLocation property"""
        return self.properties.get("resourceLocation", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[MailFolderOperationStatus]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MailFolderOperation"
