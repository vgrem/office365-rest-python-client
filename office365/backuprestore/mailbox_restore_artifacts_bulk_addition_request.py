from __future__ import annotations

from office365.backuprestore.restore_artifacts_bulk_request_base import RestoreArtifactsBulkRequestBase
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class MailboxRestoreArtifactsBulkAdditionRequest(RestoreArtifactsBulkRequestBase):
    @odata(name="directoryObjectIds")
    @property
    def directory_object_ids(self) -> StringCollection:
        """Gets the directoryObjectIds property"""
        return self.properties.get("directoryObjectIds", StringCollection())

    @odata(name="mailboxes")
    @property
    def mailboxes(self) -> StringCollection:
        """Gets the mailboxes property"""
        return self.properties.get("mailboxes", StringCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MailboxRestoreArtifactsBulkAdditionRequest"
