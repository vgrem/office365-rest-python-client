from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.print.operation_status import PrintOperationStatus
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata


class PrintOperation(PollableOperation, Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> PrintOperationStatus:
        """Gets the status property"""
        return self.properties.get("status", PrintOperationStatus())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintOperation"
