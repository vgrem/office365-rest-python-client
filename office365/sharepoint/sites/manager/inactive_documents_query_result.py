from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.inactive_document_metadata import InactiveDocumentMetadata


class InactiveDocumentsQueryResult(ClientValue):
    Files: ClientValueCollection[InactiveDocumentMetadata] = field(
        default_factory=lambda: ClientValueCollection(InactiveDocumentMetadata)
    )
    SkipToken: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.InactiveDocumentsQueryResult"
