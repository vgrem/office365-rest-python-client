from typing import Optional

from office365.runtime.client_value import ClientValue


class SPTeamsAppComponent(ClientValue):
    def __init__(
        self,
        app_description: Optional[str] = None,
        app_id: Optional[str] = None,
        app_name: Optional[str] = None,
        bot_id: Optional[str] = None,
        component_id: Optional[str] = None,
        default_size: Optional[str] = None,
        description: Optional[str] = None,
        external_app_id: Optional[str] = None,
        group_id: Optional[str] = None,
        icon_url: Optional[str] = None,
        name: Optional[str] = None,
        office_ui_fabric_icon_name: Optional[str] = None,
        version: Optional[str] = None,
    ):
        self.appDescription = app_description
        self.appId = app_id
        self.appName = app_name
        self.botId = bot_id
        self.componentId = component_id
        self.defaultSize = default_size
        self.description = description
        self.externalAppId = external_app_id
        self.groupId = group_id
        self.iconUrl = icon_url
        self.name = name
        self.officeUIFabricIconName = office_ui_fabric_icon_name
        self.version = version

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.SPTeamsAppComponent"
