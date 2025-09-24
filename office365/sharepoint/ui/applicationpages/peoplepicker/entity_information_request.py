from office365.runtime.client_value import ClientValue
from office365.sharepoint.principal.type import PrincipalType


class PickerEntityInformationRequest(ClientValue):
    """Represents a request for GetPickerEntityInformation"""

    def __init__(
        self,
        email_address: str = None,
        group_id: str = None,
        key: str = None,
        principal_type: PrincipalType = PrincipalType.None_,
    ):
        """
        :param str email_address: Gets or sets the email address of the principal.
        :param str group_id: Gets or sets the SharePoint group Id.
        :param str key: Gets or sets the identifier of the principal.
        :param int principal_type: Gets or sets the type of the principal.
        """
        super().__init__()
        self.EmailAddress = email_address
        self.GroupId = group_id
        self.Key = key
        self.PrincipalType = principal_type

    @property
    def entity_type_name(self):
        return "SP.UI.ApplicationPages.PickerEntityInformationRequest"
