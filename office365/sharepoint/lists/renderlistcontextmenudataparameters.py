from office365.runtime.client_value import ClientValue


class RenderListContextMenuDataParameters(ClientValue):

    def __init__(
        self,
        casc_del_warn_message: str = None,
        custom_action: str = None,
        field: str = None,
        id_: str = None,
        inplace_full_list_search: str = None,
        inplace_search_query: str = None,
        is_csr: str = None,
        is_xsl_view: str = None,
        item_id: str = None,
        list_view_page_url: str = None,
        override_scope: str = None,
        root_folder: str = None,
        view: str = None,
        view_count: str = None,
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
