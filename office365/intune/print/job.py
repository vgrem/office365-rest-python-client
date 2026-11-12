from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.directory.users.identity import UserIdentity
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.print.job_configuration import PrintJobConfiguration
from office365.intune.print.job_status import PrintJobStatus
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.intune.print.document import PrintDocument
    from office365.intune.print.job import PrintJob
    from office365.intune.print.task import PrintTask


class PrintJob(Entity):
    @odata(name="acknowledgedDateTime")
    @property
    def acknowledged_date_time(self) -> Optional[datetime]:
        """Gets the acknowledgedDateTime property"""
        return self.properties.get("acknowledgedDateTime", datetime.min)

    @odata(name="configuration")
    @property
    def configuration(self) -> PrintJobConfiguration:
        """Gets the configuration property"""
        return self.properties.get("configuration", PrintJobConfiguration())

    @odata(name="createdBy")
    @property
    def created_by(self) -> UserIdentity:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", UserIdentity())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="errorCode")
    @property
    def error_code(self) -> Optional[int]:
        """Gets the errorCode property"""
        return self.properties.get("errorCode", None)

    @odata(name="isFetchable")
    @property
    def is_fetchable(self) -> Optional[bool]:
        """Gets the isFetchable property"""
        return self.properties.get("isFetchable", None)

    @odata(name="redirectedFrom")
    @property
    def redirected_from(self) -> Optional[str]:
        """Gets the redirectedFrom property"""
        return self.properties.get("redirectedFrom", None)

    @odata(name="redirectedTo")
    @property
    def redirected_to(self) -> Optional[str]:
        """Gets the redirectedTo property"""
        return self.properties.get("redirectedTo", None)

    @odata(name="status")
    @property
    def status(self) -> PrintJobStatus:
        """Gets the status property"""
        return self.properties.get("status", PrintJobStatus())

    @odata(name="documents", navigation=True)
    @property
    def documents(self) -> EntityCollection[PrintDocument]:
        """Gets the documents property"""
        from office365.intune.print.document import PrintDocument

        return self.properties.get(
            "documents",
            EntityCollection[PrintDocument](self.context, PrintDocument, ResourcePath("documents", self.resource_path)),
        )

    @odata(name="tasks", navigation=True)
    @property
    def tasks(self) -> EntityCollection[PrintTask]:
        """Gets the tasks property"""
        from office365.intune.print.task import PrintTask

        return self.properties.get(
            "tasks", EntityCollection[PrintTask](self.context, PrintTask, ResourcePath("tasks", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintJob"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=[
            "PrintJob.ReadWriteBasic",
            "PrintJob.ReadWrite",
            "PrintJob.ReadWrite.All",
            "PrintJob.ReadWriteBasic.All",
        ],
    )
    def cancel(self) -> Self:
        """cancel operation."""
        qry = ServiceOperationQuery(self, "cancel", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=[
            "PrintJob.Create",
            "PrintJob.ReadWrite",
            "PrintJob.ReadWrite.All",
            "PrintJob.ReadWriteBasic",
            "PrintJob.ReadWriteBasic.All",
        ],
    )
    def start(self) -> ClientResult[PrintJobStatus]:
        """start operation."""
        from office365.intune.print.job_status import PrintJobStatus

        return_type = ClientResult(self.context, PrintJobStatus())
        qry = ServiceOperationQuery(self, "start", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(
        application=["PrintJob.ReadWriteBasic.All", "PrintJob.Manage.All", "PrintJob.ReadWrite.All"],
    )
    def abort(self, reason: str) -> Self:
        """abort operation.

        Args:
            reason (str):
                reason parameter
        """
        qry = ServiceOperationQuery(self, "abort", None, {"reason": reason}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(application=["PrintJob.Manage.All"])
    def redirect(self, destination_printer_id: str, configuration: PrintJobConfiguration) -> PrintJob:
        """redirect operation.

        Args:
            destination_printer_id (str):
                destinationPrinterId parameter
            configuration (PrintJobConfiguration):
                configuration parameter
        """
        from office365.intune.print.job import PrintJob

        return_type = PrintJob(self.context)
        qry = ServiceOperationQuery(
            self,
            "redirect",
            None,
            {"destinationPrinterId": destination_printer_id, "configuration": configuration},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
