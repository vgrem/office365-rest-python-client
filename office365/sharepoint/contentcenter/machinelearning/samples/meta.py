from office365.runtime.client_value import ClientValue


class MachineLearningSampleMeta(ClientValue):
    def __init__(self, extracted_text: str = None):
        self.ExtractedText = extracted_text

    @property
    def entity_type_name(self):
        return "SP.MachineLearningSampleMeta"
