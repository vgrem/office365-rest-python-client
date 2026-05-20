from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class HashTag(ClientValue):
    """The HashTag type specifies a string that is being used as a hash tag and a count of the tags use.

    :param Optional[str] Name: The Name property specifies the hash tag string.
    :param Optional[int] UseCount: The UseCount property specifies the number of times that the hash tag is used.
    """

    Name: Optional[str] = None
    UseCount: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.HashTag"
