from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.publishing.error import Error


class RuleErrorDetails(ClientValue):

    def __init__(
        self,
        error_headers: StringCollection = StringCollection(),
        errors: Error = Error(),
    ):
        self.errorHeaders = error_headers
        self.errors = errors

    @property
    def entity_type_name(self):
        return "SP.Publishing.RuleErrorDetails"
