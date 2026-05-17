from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class ContentControlInfo(ClientValue):
    def __init__(
        self,
        content_control_tag_name: Optional[str] = None,
        end_index: Optional[int] = None,
        is_single_parargaph: Optional[bool] = None,
        paragraph_ids: StringCollection = StringCollection(),
        start_index: Optional[int] = None,
    ):
        self.content_control_tag_name = content_control_tag_name
        self.end_index = end_index
        self.is_single_parargaph = is_single_parargaph
        self.paragraph_ids = paragraph_ids
        self.start_index = start_index
