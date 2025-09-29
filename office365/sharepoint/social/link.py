from office365.runtime.client_value import ClientValue


class SocialLink(ClientValue):

    def __init__(self, text: str = None, uri: str = None):
        """The SocialLink class defines a link that includes a URI and text representation.
        This class is used to represent the location of a web site."""
        self.Text = text
        self.Uri = uri

    @property
    def entity_type_name(self):
        return "SP.Social.SocialLink"
