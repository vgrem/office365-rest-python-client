from office365.sharepoint.publishing.pages.fields_data import SitePageFieldsData


class SitePage3DFieldsData(SitePageFieldsData):

    def __init__(self, space_content: str = None):
        super().__init__()
        self.SpaceContent = space_content

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePage3DFieldsData"
