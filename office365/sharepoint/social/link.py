from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SocialLink(ClientValue):
    """The SocialLink class defines a link that includes a URI and text representation.
    This class is used to represent the location of a web site."""

    Text: Optional[str] = None
    Uri: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialLink"
