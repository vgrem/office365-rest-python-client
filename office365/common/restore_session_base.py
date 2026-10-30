from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.backuprestore.restorejobtype import RestoreJobType
from office365.backuprestore.restoresessions.artifact_count import RestoreSessionArtifactCount
from office365.backuprestore.restoresessions.status import RestoreSessionStatus
from office365.directory.identity_set import IdentitySet
from office365.entity import Entity
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.types.public_error import PublicError


class RestoreSessionBase(Entity):
    def activate(self) -> Self:
        """Activate the restore session so the restore job starts.

        A freshly created restore session is in the ``draft`` state; activating it
        moves it through ``activating`` to ``active`` / ``completed``.
        """
        qry = ServiceOperationQuery(self, "activate", return_type=self)
        self.context.add_query(qry)
        return self

    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> Optional[datetime]:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="error")
    @property
    def error(self) -> PublicError:
        """Gets the error property"""
        return self.properties.get("error", PublicError())

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="restoreJobType")
    @property
    def restore_job_type(self) -> RestoreJobType:
        """Gets the restoreJobType property"""
        return self.properties.get("restoreJobType", RestoreJobType.standard)

    @odata(name="restoreSessionArtifactCount")
    @property
    def restore_session_artifact_count(self) -> RestoreSessionArtifactCount:
        """Gets the restoreSessionArtifactCount property"""
        return self.properties.get("restoreSessionArtifactCount", RestoreSessionArtifactCount())

    @odata(name="status")
    @property
    def status(self) -> RestoreSessionStatus:
        """Gets the status property"""
        return self.properties.get("status", RestoreSessionStatus.draft)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestoreSessionBase"

    @odata(name="policyId")
    @property
    def policy_id(self) -> Optional[str]:
        """Gets the policyId property"""
        return self.properties.get("policyId", None)
