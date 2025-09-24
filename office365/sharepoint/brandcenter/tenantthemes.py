from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.brandcenter.theme_data import ThemeData


class TenantThemes(ClientValue):

    def __init__(
        self,
        hide_default_themes: bool = None,
        theme_data: ClientValueCollection[ThemeData] = ClientValueCollection(ThemeData),
    ):
        self.hide_default_themes = hide_default_themes
        self.theme_data = theme_data
