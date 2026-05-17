from typing import Optional

from office365.runtime.client_value import ClientValue


class ContentAssemblyFormAnswer(ClientValue):
    def __init__(
        self,
        additional_data: Optional[str] = None,
        answer: Optional[str] = None,
        content_control_tag_name: Optional[str] = None,
    ):
        self.additional_data = additional_data
        self.answer = answer
        self.content_control_tag_name = content_control_tag_name
