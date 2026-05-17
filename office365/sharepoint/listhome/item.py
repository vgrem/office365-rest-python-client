from typing import Optional

from office365.runtime.client_value import ClientValue


class ListHomeItem(ClientValue):
    def __init__(
        self,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        is_default_document_library: Optional[bool] = None,
        is_doc_lib: Optional[bool] = None,
        list_id: Optional[str] = None,
        list_url: Optional[str] = None,
        site_acronym: Optional[str] = None,
        site_color: Optional[str] = None,
        site_icon_url: Optional[str] = None,
        site_id: Optional[str] = None,
        site_title: Optional[str] = None,
        site_url: Optional[str] = None,
        title: Optional[str] = None,
        web_id: Optional[str] = None,
        web_template_configuration: Optional[str] = None,
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
