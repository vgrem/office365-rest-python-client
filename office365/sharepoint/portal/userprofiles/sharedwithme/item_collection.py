from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class SharedWithMeItemCollection(Entity):
    """"""

    @staticmethod
    def get_shared_with_me_external_items(context, top: int) -> ClientResult[str]:
        """Args:
        context (office365.sharepoint.client_context.ClientContext): Client context
        top (int):
        """
        binding_type = SharedWithMeItemCollection(context)
        return_type = ClientResult(context, str())
        params = {"top": top}
        qry = ServiceOperationQuery(
            binding_type,
            "GetSharedWithMeExternalItems",
            params,
            return_type=return_type,
            is_static=True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_shared_with_me_items(context, top, skip_token=None, include_sharing_history=None):
        """Args:
        context (office365.sharepoint.client_context.ClientContext): Client context
        top (int):
        skip_token (str):
        include_sharing_history (bool):
        """
        binding_type = SharedWithMeItemCollection(context)
        return_type = ClientResult(context, str())
        params = {
            "top": top,
            "skiptoken": skip_token,
            "includeSharingHistory": include_sharing_history,
        }
        qry = ServiceOperationQuery(
            binding_type,
            "GetSharedWithMeItems",
            None,
            params,
            return_type=return_type,
            is_static=True,
        )
        context.add_query(qry)
        return return_type
