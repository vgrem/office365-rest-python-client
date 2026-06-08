from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class GroupCreationInformation(ClientValue):
    """An object used to facilitate creation of a cross-site group.

    Args:
        title (str):
        description (str):
    """

    Title: Optional[str] = None
    Description: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Group"
