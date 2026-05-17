from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholder import Placeholder
from typing import Optional


class UpdateTemplateInfo(ClientValue):
    def __init__(
        self,
        new_name: Optional[str] = None,
        operation: Optional[int] = None,
        placeholders: ClientValueCollection[Placeholder] = ClientValueCollection(Placeholder),
    ):
        self.new_name = new_name
        self.operation = operation
        self.placeholders = placeholders
