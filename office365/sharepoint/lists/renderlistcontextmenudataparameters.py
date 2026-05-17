from typing import Optional

from office365.runtime.client_value import ClientValue


class RenderListContextMenuDataParameters(ClientValue):
    def __init__(
        self,
        casc_del_warn_message: Optional[str] = None,
        custom_action: Optional[str] = None,
        field: Optional[str] = None,
        id_: Optional[str] = None,
        inplace_full_list_search: Optional[str] = None,
        inplace_search_query: Optional[str] = None,
        is_csr: Optional[str] = None,
        is_xsl_view: Optional[str] = None,
        item_id: Optional[str] = None,
        list_view_page_url: Optional[str] = None,
        override_scope: Optional[str] = None,
        root_folder: Optional[str] = None,
        view: Optional[str] = None,
        view_count: Optional[str] = None,
    ):
        self.casc_del_warn_message = casc_del_warn_message
        self.custom_action = custom_action
        self.field = field
        self.id = id_
        self.inplace_full_list_search = inplace_full_list_search
        self.inplace_search_query = inplace_search_query
        self.is_csr = is_csr
        self.is_xsl_view = is_xsl_view
        self.item_id = item_id
        self.list_view_page_url = list_view_page_url
        self.override_scope = override_scope
        self.root_folder = root_folder
        self.view = view
        self.view_count = view_count
