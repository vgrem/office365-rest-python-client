from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class LogActivityExtraProperties(ClientValue):
    CampaignMetadata: Optional[str] = None
    IsWebWelcomePage: Optional[bool] = None
    LinkUrlClicked: Optional[str] = None
    SPOWebPartInstanceId: str | None = None
    SPOWebPartManifestId: str | None = None
    SPOWebPartSubComponentId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.LogActivityExtraProperties"
