from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.brandcenter.theme_data import ThemeData


class SiteThemes(ClientValue):

    def __init__(
        self,
        theme_data: ClientValueCollection[ThemeData] = ClientValueCollection(ThemeData),
    ):
        self.themeData = theme_data

    " "
