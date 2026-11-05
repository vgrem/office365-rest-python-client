from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.odata_property import odata


class UserIdInfo(ClientValue):
    """Represents an identity providers unique identifier information

    Args:
        name_id (str): Specifies the identity provider's unique identifier.
        name_id_issuer (str): Specifies the identity provider's display name as registered in a farm.
    """

    name_id: Optional[str] = field(default=None, metadata=odata(name="NameId"))
    name_id_issuer: Optional[str] = field(default=None, metadata=odata(name="NameIdIssuer"))
