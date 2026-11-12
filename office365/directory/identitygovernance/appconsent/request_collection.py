from office365.directory.identitygovernance.appconsent.request import AppConsentRequest
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.verbs import verb


class AppConsentRequestCollection(EntityCollection[AppConsentRequest]):
    """AppConsentRequest's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, AppConsentRequest, resource_path)

    @verb(role="action", effect="read")
    @require_permission(delegated=["ConsentRequest.Read.All", "ConsentRequest.ReadWrite.All"])
    def filter_by_current_user(self, on: str) -> "AppConsentRequestCollection":
        """Retrieve a collection of appConsentRequest objects for which the current user is the reviewer and the status
        of the userConsentRequest for accessing the specified app is InProgress.

        Args:
            on (str): Filter to query appConsentRequest objects for which the current user is a reviewer.
              Allowed value is reviewer. Required.
        """
        return_type = AppConsentRequestCollection(self.context)
        params = {"on": on}
        qry = FunctionQuery(self, "filterByCurrentUser", params, return_type)
        self.context.add_query(qry)
        return return_type
