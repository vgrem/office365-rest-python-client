from typing import Optional

from office365.runtime.client_value import ClientValue


class RenderListFilterDataParameters(ClientValue):
    def __init__(
        self,
        exclude_field_filtering_html: Optional[bool] = None,
        field_internal_name: Optional[str] = None,
        override_scope: Optional[str] = None,
        process_q_string_to_caml: Optional[str] = None,
        view_id: Optional[str] = None,
        view_xml: Optional[str] = None,
    ):
        self.ExcludeFieldFilteringHtml = exclude_field_filtering_html
        self.FieldInternalName = field_internal_name
        self.OverrideScope = override_scope
        self.ProcessQStringToCAML = process_q_string_to_caml
        self.ViewId = view_id
        self.ViewXml = view_xml

    "Specifies the parameters that are used to retrieve filter data."
