from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPTeamsAppComponent(ClientValue):
    appDescription: str | None = None
    appId: str | None = None
    appName: str | None = None
    botId: str | None = None
    componentId: str | None = None
    defaultSize: str | None = None
    externalAppId: str | None = None
    groupId: str | None = None
    iconUrl: str | None = None
    officeUIFabricIconName: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.SPTeamsAppComponent"
