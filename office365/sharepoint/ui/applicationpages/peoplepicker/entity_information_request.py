from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.principal.type import PrincipalType


@dataclass
class PickerEntityInformationRequest(ClientValue):
    """Represents a request for GetPickerEntityInformation

    :param str email_address: Gets or sets the email address of the principal.
    :param str group_id: Gets or sets the SharePoint group Id.
    :param str key: Gets or sets the identifier of the principal.
    :param int principal_type: Gets or sets the type of the principal.
    """

    EmailAddress: Optional[str] = None
    GroupId: Optional[str] = None
    Key: Optional[str] = None
    PrincipalType: PrincipalType = PrincipalType.Unknown

    @property
    def entity_type_name(self):
        return "SP.UI.ApplicationPages.PickerEntityInformationRequest"
