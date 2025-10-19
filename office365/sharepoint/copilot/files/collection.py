from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.copilot.files.collection_query_result import (
    CopilotFileCollectionQueryResult,
)
from office365.sharepoint.entity import Entity


class CopilotFileCollection(Entity):
    """ """

    @staticmethod
    def get_working_set_files(
        context, top: int = None, order_by: str = None, skip_token: str = None
    ) -> ClientResult[CopilotFileCollectionQueryResult]:
        """ """
        payload = {"top": top, "orderBy": order_by, "skipToken": skip_token}
        return_type = ClientResult(context, CopilotFileCollectionQueryResult())
        qry = ServiceOperationQuery(
            CopilotFileCollection(context),
            "GetWorkingSetFiles",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type
