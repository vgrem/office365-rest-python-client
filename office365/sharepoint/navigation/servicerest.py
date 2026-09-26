from __future__ import annotations

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.navigation.home_site_navigation_settings import HomeSiteNavigationSettings
from office365.sharepoint.navigation.menu.state import MenuState


class NavigationServiceRest(Entity):
    @property
    def home_site_settings(self) -> HomeSiteNavigationSettings:
        """Gets the HomeSiteSettings property"""
        return self.properties.get(
            "HomeSiteSettings",
            HomeSiteNavigationSettings(self.context, ResourcePath("HomeSiteSettings", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Navigation.REST.NavigationServiceRest"

    def current_resources_nav(self, source: int, include_viva_resources: bool) -> ClientResult[MenuState]:
        """CurrentResourcesNav operation.

        Args:
            source (int): source parameter
            include_viva_resources (bool): includeVivaResources parameter
        """
        return_type = ClientResult(self.context, MenuState())
        qry = FunctionQuery(self, "CurrentResourcesNav", [source, include_viva_resources], return_type)
        self.context.add_query(qry)
        return return_type

    def get_publishing_navigation_provider_type(self, map_provider_name: str) -> ClientResult[int]:
        """GetPublishingNavigationProviderType operation.

        Args:
            map_provider_name (str): mapProviderName parameter
        """
        return_type = ClientResult(self.context, int())
        qry = FunctionQuery(self, "GetPublishingNavigationProviderType", [map_provider_name], return_type)
        self.context.add_query(qry)
        return return_type

    def global_nav(self, source: str, include_viva_resources: bool) -> ClientResult[MenuState]:
        """GlobalNav operation.

        Args:
            source (str): source parameter
            include_viva_resources (bool): includeVivaResources parameter
        """
        return_type = ClientResult(self.context, MenuState())
        qry = FunctionQuery(self, "GlobalNav", [source, include_viva_resources], return_type)
        self.context.add_query(qry)
        return return_type

    def global_nav_enabled(self) -> ClientResult[bool]:
        """GlobalNavEnabled operation."""
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "GlobalNavEnabled", [], return_type)
        self.context.add_query(qry)
        return return_type

    def home_site_navigation(self, source: int) -> ClientResult[MenuState]:
        """HomeSiteNavigation operation.

        Args:
            source (int): source parameter
        """
        return_type = ClientResult(self.context, MenuState())
        qry = FunctionQuery(self, "HomeSiteNavigation", [source], return_type)
        self.context.add_query(qry)
        return return_type

    def menu_node_key(self, current_url: str, map_provider_name: str) -> ClientResult[str]:
        """MenuNodeKey operation.

        Args:
            current_url (str): currentUrl parameter
            map_provider_name (str): mapProviderName parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "MenuNodeKey", [current_url, map_provider_name], return_type)
        self.context.add_query(qry)
        return return_type

    def menu_state(
        self, menu_node_key: str, map_provider_name: str, depth: int, custom_properties: str
    ) -> ClientResult[MenuState]:
        """MenuState operation.

        Args:
            menu_node_key (str): menuNodeKey parameter
            map_provider_name (str): mapProviderName parameter
            depth (int): depth parameter
            custom_properties (str): customProperties parameter
        """
        return_type = ClientResult(self.context, MenuState())
        qry = FunctionQuery(self, "MenuState", [menu_node_key, map_provider_name, depth, custom_properties], return_type)
        self.context.add_query(qry)
        return return_type

    def save_menu_state(self, menu_state: MenuState, map_provider_name: str) -> ClientResult[int]:
        """SaveMenuState operation.

        Args:
            menu_state (MenuState): menuState parameter
            map_provider_name (str): mapProviderName parameter
        """
        return_type = ClientResult(self.context, int())
        qry = ServiceOperationQuery(
            self,
            "SaveMenuState",
            None,
            {"menuState": menu_state, "mapProviderName": map_provider_name},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def set_global_nav_enabled(self, is_enabled: bool) -> Self:
        """SetGlobalNavEnabled operation.

        Args:
            is_enabled (bool): isEnabled parameter
        """
        qry = ServiceOperationQuery(self, "SetGlobalNavEnabled", None, {"isEnabled": is_enabled}, None, None)
        self.context.add_query(qry)
        return self

    def tree_view(self, depth: int) -> ClientResult[MenuState]:
        """TreeView operation.

        Args:
            depth (int): depth parameter
        """
        return_type = ClientResult(self.context, MenuState())
        qry = FunctionQuery(self, "TreeView", [depth], return_type)
        self.context.add_query(qry)
        return return_type
