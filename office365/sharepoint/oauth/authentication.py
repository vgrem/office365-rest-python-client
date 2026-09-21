from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class Authentication(Entity):
    """
    Exposes relationships that represent the authentication methods.
    """

    @property
    def entity_type_name(self) -> str:
        return "SP.OAuth.Authentication"

    def get_renewal_url(self, redirect_url: str) -> ClientResult[str]:
        """GetRenewalUrl operation.

        Args:
            redirect_url (str): redirectUrl parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "GetRenewalUrl", None, {"redirectUrl": redirect_url}, None, return_type)
        self.context.add_query(qry)
        return return_type
