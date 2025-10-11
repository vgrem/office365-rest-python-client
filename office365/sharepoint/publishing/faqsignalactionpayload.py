from office365.runtime.client_value import ClientValue


class FaqSignalActionPayload(ClientValue):

    def __init__(self, action_type: int = None, question_id: str = None, signal_type: int = None):
        self.ActionType = action_type
        self.QuestionId = question_id
        self.SignalType = signal_type

    @property
    def entity_type_name(self):
        return "SP.Publishing.FaqSignalActionPayload"
