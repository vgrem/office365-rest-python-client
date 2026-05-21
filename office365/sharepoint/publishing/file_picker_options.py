from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.administration.orgassets.org_assets import OrgAssets


@dataclass
class FilePickerOptions(ClientValue):
    BingSearchEnabled: bool | None = None
    CentralAssetRepository: OrgAssets = field(default_factory=OrgAssets)
    OrgAssets: OrgAssets = field(default_factory=OrgAssets)

    @property
    def entity_type_name(self):
        return "SP.Publishing.FilePickerOptions"
