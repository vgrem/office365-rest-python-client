from office365.runtime.client_value import ClientValue


class Placeholder(ClientValue):
    def __init__(
        self,
        data_type: str = None,
        end_position: int = None,
        id_: str = None,
        name: str = None,
        paragraph_id: str = None,
        question_title: str = None,
        source: str = None,
        start_position: int = None,
    ):
        self.data_type = data_type
        self.end_position = end_position
        self.id = id_
        self.name = name
        self.paragraph_id = paragraph_id
        self.question_title = question_title
        self.source = source
        self.start_position = start_position
