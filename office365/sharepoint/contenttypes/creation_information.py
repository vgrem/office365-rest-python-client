from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class ContentTypeCreationInformation(ClientValue):

    """
    Specifies properties that are used as parameters to initialize a new content type.

    :param str ct_id: Specifies the ContentTypeId (section 3.2.5.30) of the content type to be constructed.
    :param str name: Specifies the name of the content type to be constructed.
    :param str description: Specifies the description of the content type to be constructed.
    :param str group: Specifies the group of the content type to be constructed.
    """

    Name: str
    Description: Optional[str] = None
    group: Optional[str] = None
    Id: Optional[str] = None