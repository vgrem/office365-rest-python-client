from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class RenderListContextMenuDataParameters(ClientValue):
    casc_del_warn_message: Optional[str] = None
    custom_action: Optional[str] = None
    field: Optional[str] = None
    id: Optional[str] = None
    inplace_full_list_search: Optional[str] = None
    inplace_search_query: Optional[str] = None
    is_csr: Optional[str] = None
    is_xsl_view: Optional[str] = None
    item_id: Optional[str] = None
    list_view_page_url: Optional[str] = None
    override_scope: Optional[str] = None
    root_folder: Optional[str] = None
    view: Optional[str] = None
    view_count: Optional[str] = None
