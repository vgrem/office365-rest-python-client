from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity
from office365.sharepoint.navigation.home_site_navigation_settings import HomeSiteNavigationSettings


class NavigationServiceRest(Entity):

    @property
    def home_site_settings(self) -> HomeSiteNavigationSettings:
        """Gets the HomeSiteSettings property"""
        return self.properties.get(
            "HomeSiteSettings",
            HomeSiteNavigationSettings(self.context, ResourcePath("HomeSiteSettings", self.resource_path)),
        )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Navigation.REST.NavigationServiceRest"
