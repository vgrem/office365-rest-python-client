from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.portal.m365tabitem import M365TabItem


@value
class PinToTeamResponse(ClientValue):
    FailedPinning: ClientValueCollection[M365TabItem] = field(default_factory=lambda: ClientValueCollection(M365TabItem))
    SuccessfulPinning: ClientValueCollection[M365TabItem] = field(
        default_factory=lambda: ClientValueCollection(M365TabItem)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.PinToTeamResponse"
