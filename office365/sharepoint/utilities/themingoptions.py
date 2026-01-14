from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.utilities.jsontheme import JsonTheme


class ThemingOptions(ClientValue):
    def __init__(
        self,
        hide_default_themes: bool = None,
        theme_previews: ClientValueCollection[JsonTheme] = ClientValueCollection(JsonTheme),
    ):
        self.hideDefaultThemes = hide_default_themes
        self.themePreviews = theme_previews

    @property
    def entity_type_name(self):
        return "SP.Utilities.ThemingOptions"
