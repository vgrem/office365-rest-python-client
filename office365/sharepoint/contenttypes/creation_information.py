from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ContentTypeCreationInformation(ClientValue):
    """Specifies properties that are used as parameters to initialize a new content type.

    Args:
        ct_id (str): Specifies the ContentTypeId (section 3.2.5.30) of the content type to be constructed.
        name (str): Specifies the name of the content type to be constructed.
        description (str): Specifies the description of the content type to be constructed.
        group (str): Specifies the group of the content type to be constructed.
    """

    Name: str
    Description: Optional[str] = None
    group: Optional[str] = None
    Id: Optional[str] = None
    Group: str | None = None
