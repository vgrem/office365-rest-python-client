from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPTeamsAppComponent(ClientValue):
    app_description: str | None = None
    app_id: str | None = None
    app_name: str | None = None
    bot_id: str | None = None
    component_id: str | None = None
    default_size: str | None = None
    description: str | None = None
    external_app_id: str | None = None
    group_id: str | None = None
    icon_url: str | None = None
    name: str | None = None
    office_ui_fabric_icon_name: str | None = None
    version: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.SPTeamsAppComponent"
