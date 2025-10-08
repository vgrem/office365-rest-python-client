from office365.runtime.client_value import ClientValue


class SPTeamsAppComponent(ClientValue):

    def __init__(
        self,
        app_description: str = None,
        app_id: str = None,
        app_name: str = None,
        bot_id: str = None,
        component_id: str = None,
        default_size: str = None,
        description: str = None,
        external_app_id: str = None,
        group_id: str = None,
        icon_url: str = None,
        name: str = None,
        office_ui_fabric_icon_name: str = None,
        version: str = None,
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
