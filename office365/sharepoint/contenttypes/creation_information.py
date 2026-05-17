from typing import Optional

from office365.runtime.client_value import ClientValue


class ContentTypeCreationInformation(ClientValue):
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        group: Optional[str] = None,
        ct_id: Optional[str] = None,
        id_: Optional[str] = None,
    ):
        """Specifies properties that are used as parameters to initialize a new content type.

        :param str ct_id: Specifies the ContentTypeId (section 3.2.5.30) of the content type to be constructed.
        :param str name: Specifies the name of the content type to be constructed.
        :param str description: Specifies the description of the content type to be constructed.
        :param str group: Specifies the group of the content type to be constructed.
        """
        super().__init__()
        self.Name = name
        self.Description = description
        self.group = group
        self.Id = ct_id
        self.Id = id_
