from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.manager.baaa_item_provider_request import BAAAItemProviderRequest
from office365.sharepoint.sites.manager.baaa_task_parameters import BAAATaskParameters


class BAAARequest(ClientValue):
    ForceRunAsync: bool | None = None
    IsDebug: bool | None = None
    TaskParameters: BAAATaskParameters = field(default_factory=BAAATaskParameters)
    BAAAItemProviderRequest: BAAAItemProviderRequest = field(default_factory=BAAAItemProviderRequest)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.BAAARequest"
