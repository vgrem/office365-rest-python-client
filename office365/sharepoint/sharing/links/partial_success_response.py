from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.entityresult import SharingEntityResult
from office365.sharepoint.sharing.links.share_response import ShareLinkResponse


@dataclass
class ShareLinkPartialSuccessResponse(ShareLinkResponse):
    entityResults: ClientValueCollection[SharingEntityResult] = field(
        default_factory=lambda: ClientValueCollection(SharingEntityResult)
    )

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "SP.Sharing.ShareLinkPartialSuccessResponse"
