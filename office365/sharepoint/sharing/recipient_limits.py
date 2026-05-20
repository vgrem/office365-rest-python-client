from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.recipientlimitsinfo import RecipientLimitsInfo


@dataclass
class RecipientLimits(ClientValue):
    checkPermissions: RecipientLimitsInfo = field(default_factory=RecipientLimitsInfo)
    grantDirectAccess: RecipientLimitsInfo = field(default_factory=RecipientLimitsInfo)
    shareLink: RecipientLimitsInfo = field(default_factory=RecipientLimitsInfo)
    shareLinkWithDeferRedeem: RecipientLimitsInfo = field(default_factory=RecipientLimitsInfo)

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.RecipientLimits"
