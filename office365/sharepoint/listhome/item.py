from office365.runtime.client_value import ClientValue


class ListHomeItem(ClientValue):

    def __init__(
        self,
        color: str = None,
        icon: str = None,
        is_default_document_library: bool = None,
        is_doc_lib: bool = None,
        list_id: str = None,
        list_url: str = None,
        site_acronym: str = None,
        site_color: str = None,
        site_icon_url: str = None,
        site_id: str = None,
        site_title: str = None,
        site_url: str = None,
        title: str = None,
        web_id: str = None,
        web_template_configuration: str = None,
    ):
        self.color = color
        self.icon = icon
        self.isDefaultDocumentLibrary = is_default_document_library
        self.isDocLib = is_doc_lib
        self.listId = list_id
        self.listUrl = list_url
        self.siteAcronym = site_acronym
        self.siteColor = site_color
        self.siteIconUrl = site_icon_url
        self.siteId = site_id
        self.siteTitle = site_title
        self.siteUrl = site_url
        self.title = title
        self.webId = web_id
        self.webTemplateConfiguration = web_template_configuration

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ListHome.ListHomeItem"
