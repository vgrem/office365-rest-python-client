from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UserIdInfo(ClientValue):
    """Represents an identity providers unique identifier information

    :param str name_id: Specifies the identity provider's unique identifier.
    :param str name_id_issuer: Specifies the identity provider's display name as registered in a farm.
    """

    NameId: Optional[str] = None
    NameIdIssuer: Optional[str] = None
