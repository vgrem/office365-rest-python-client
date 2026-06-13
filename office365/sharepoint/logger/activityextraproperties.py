from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
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
