from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.dynamiccontent.source_file import SourceFile


class SourceFileRquest(ClientValue):
    PageItemId: int | None = None
    PageItemUniqueId: str | None = None
    SourceFiles: ClientValueCollection[SourceFile] = field(default_factory=lambda: ClientValueCollection(SourceFile))
    Title: str | None = None
    WebPartInstanceId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.timerjob.SourceFileRquest"
