from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.principal.type import PrincipalType
from office365.sharepoint.ui.applicationpages.peoplepicker.entity_information import (
    PickerEntityInformation,
)
from office365.sharepoint.ui.applicationpages.peoplepicker.entity_information_request import (
    PickerEntityInformationRequest,
)
from office365.sharepoint.ui.applicationpages.peoplepicker.query_parameters import (
    ClientPeoplePickerQueryParameters,
)

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class ClientPeoplePickerWebServiceInterface(Entity):
    """Specifies an interface that can be used to query principals."""

    @staticmethod
    def get_search_results_by_hierarchy(
        context: ClientContext,
        provider_id: Optional[str] = None,
        hierarchy_node_id: Optional[str] = None,
        entity_types: Optional[str] = None,
        context_url: Optional[str] = None,
    ):
        """Specifies a JSON formatted CSOM String of principals found in the search grouped by hierarchy.

        Args:
            context (office365.sharepoint.client_context.ClientContext):
            provider_id (str): The identifier of a claims provider.
            hierarchy_node_id (str): The identifier of a node in the hierarchy. The search MUST be conducted under
                this node.
            entity_types (str): The type of principals to search for.
            context_url (str): The URL to use as context when searching for principals.
        """
        return_type = ClientResult(context, str())
        payload = {
            "providerID": provider_id,
            "hierarchyNodeID": hierarchy_node_id,
            "entityTypes": entity_types,
            "contextUrl": context_url,
        }
        svc = ClientPeoplePickerWebServiceInterface(context)
        qry = ServiceOperationQuery(svc, "GetSearchResultsByHierarchy", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def client_people_picker_resolve_user(context: ClientContext, query_string: str) -> ClientResult[str]:
        """Resolves the principals to a string of JSON representing users in people picker format.

        Args:
            query_string (str): Specifies the value to be used in the principal query.
            context (office365.sharepoint.client_context.ClientContext): SharePoint client context
        """
        return_type = ClientResult(context, str())
        binding_type = ClientPeoplePickerWebServiceInterface(context)
        payload = {"queryParams": ClientPeoplePickerQueryParameters(QueryString=query_string)}
        qry = ServiceOperationQuery(
            binding_type,
            "ClientPeoplePickerResolveUser",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def client_people_picker_search_user(
        context: ClientContext, query_string: str, maximum_entity_suggestions: int = 100
    ):
        """Returns for a string of JSON representing users in people picker format of the specified principals.

        Args:
            context (office365.sharepoint.client_context.ClientContext): SharePoint client context
            query_string (str): Specifies the value to be used in the principal query.
            maximum_entity_suggestions (int): Specifies the maximum number of principals to be returned by the
                principal query.
        """
        return_type = ClientResult(context, str())
        binding_type = ClientPeoplePickerWebServiceInterface(context)
        params = ClientPeoplePickerQueryParameters(
            QueryString=query_string,
            MaximumEntitySuggestions=maximum_entity_suggestions,
        )
        payload = {"queryParams": params}
        qry = ServiceOperationQuery(
            binding_type,
            "ClientPeoplePickerSearchUser",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_picker_entity_information(context, email_address: str):
        """Gets information of the specified principal.

        Args:
            context (office365.sharepoint.client_context.ClientContext): SharePoint client context
            email_address (str): Specifies the principal for which information is being requested.
        """
        request = PickerEntityInformationRequest(EmailAddress=email_address, PrincipalType=PrincipalType.All)
        return_type = PickerEntityInformation(context)
        binding_type = ClientPeoplePickerWebServiceInterface(context)
        payload = {"entityInformationRequest": request}
        qry = ServiceOperationQuery(
            binding_type,
            "GetPickerEntityInformation",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.UI.ApplicationPages.ClientPeoplePickerWebServiceInterface"


class PeoplePickerWebServiceInterface(Entity):
    @staticmethod
    def get_search_results(
        context,
        search_pattern,
        provider_id=None,
        hierarchy_node_id=None,
        entity_types=None,
    ):
        """Specifies a JSON formatted CSOM String of principals found in the search.

        Args:
            context (office365.sharepoint.client_context.ClientContext):
            search_pattern (str): Specifies a pattern used to search for principals. The value is
                implementation-specific.
            provider_id (str): The identifier of a claims provider.
            hierarchy_node_id (str): The identifier of a node in the hierarchy. The search MUST be conducted under
                this node.
            entity_types (str): The type of principals to search for.
        """
        return_type = ClientResult(context, str())
        payload = {
            "searchPattern": search_pattern,
            "providerID": provider_id,
            "hierarchyNodeID": hierarchy_node_id,
            "entityTypes": entity_types,
        }
        svc = PeoplePickerWebServiceInterface(context)
        qry = ServiceOperationQuery(svc, "GetSearchResults", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.UI.ApplicationPages.PeoplePickerWebServiceInterface"
