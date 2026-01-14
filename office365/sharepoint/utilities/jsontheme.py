from office365.runtime.client_value import ClientValue


class JsonTheme(ClientValue):
    def __init__(self, name: str = None, theme_json: str = None):
        self.name = name
        self.themeJson = theme_json

    @property
    def entity_type_name(self):
        return "SP.Utilities.JsonTheme"
