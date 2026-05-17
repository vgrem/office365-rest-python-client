from typing import Optional

from office365.runtime.client_value import ClientValue


class Placeholder(ClientValue):
    def __init__(
        self,
        data_type: Optional[str] = None,
        end_position: Optional[int] = None,
        id_: Optional[str] = None,
        name: Optional[str] = None,
        paragraph_id: Optional[str] = None,
        question_title: Optional[str] = None,
        source: Optional[str] = None,
        start_position: Optional[int] = None,
    ):
        self.data_type = data_type
        self.end_position = end_position
        self.id = id_
        self.name = name
        self.paragraph_id = paragraph_id
        self.question_title = question_title
        self.source = source
        self.start_position = start_position
