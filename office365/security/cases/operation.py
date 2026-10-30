from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata
from office365.security.cases.action import CaseAction
from office365.security.cases.operationstatus import CaseOperationStatus

if TYPE_CHECKING:
    from office365.communications.result_info import ResultInfo
    from office365.directory.identity_set import IdentitySet


class CaseOperation(PollableOperation, Entity):
    """An abstract entity that represents a long-running eDiscovery process.
    It contains a common set of properties that are shared among inheriting entities"""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.caseOperation"

    @odata(name="action")
    @property
    def action(self) -> CaseAction:
        """Gets the action property"""
        return self.properties.get("action", CaseAction.contentExport)

    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> Optional[datetime]:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="percentProgress")
    @property
    def percent_progress(self) -> Optional[int]:
        """Gets the percentProgress property"""
        return self.properties.get("percentProgress", None)

    @odata(name="resultInfo")
    @property
    def result_info(self) -> ResultInfo:
        """Gets the resultInfo property"""
        from office365.communications.result_info import ResultInfo

        return self.properties.get("resultInfo", ResultInfo())

    @odata(name="status")
    @property
    def status(self) -> CaseOperationStatus:
        """Gets the status property"""
        return self.properties.get("status", CaseOperationStatus.notStarted)
