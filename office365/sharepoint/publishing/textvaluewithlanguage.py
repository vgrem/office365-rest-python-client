from office365.runtime.client_value import ClientValue


class TextValueWithLanguage(ClientValue):

    def __init__(self, color_seed: str = None, lcid: int = None, text: str = None):
        self.ColorSeed = color_seed
        self.Lcid = lcid
        self.Text = text

    @property
    def entity_type_name(self):
        return "SP.Publishing.TextValueWithLanguage"
