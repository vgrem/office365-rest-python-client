from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.sharing.recipientlimitsinfo import RecipientLimitsInfo


@value
class RecipientLimits(ClientValue):
    checkPermissions: RecipientLimitsInfo = field(default_factory=RecipientLimitsInfo)
    grantDirectAccess: RecipientLimitsInfo = field(default_factory=RecipientLimitsInfo)
    shareLink: RecipientLimitsInfo = field(default_factory=RecipientLimitsInfo)
    shareLinkWithDeferRedeem: RecipientLimitsInfo = field(default_factory=RecipientLimitsInfo)

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.RecipientLimits"
