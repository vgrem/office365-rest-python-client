from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UserIdInfo(ClientValue):
    """Represents an identity providers unique identifier information

    Args:
        name_id (str): Specifies the identity provider's unique identifier.
        name_id_issuer (str): Specifies the identity provider's display name as registered in a farm.
    """

    NameId: Optional[str] = None
    NameIdIssuer: Optional[str] = None
