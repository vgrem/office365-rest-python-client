from __future__ import annotations

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class NonQuotaBackfillApi(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuotaManagement.Consumer.NonQuotaBackfillApi"

    def backfill_non_quota(self, backfill_userfacts: list[str]) -> ClientResult[str]:
        """BackfillNonQuota operation.

        Args:
            backfill_userfacts (list[str]): backfillUserfacts parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "BackfillNonQuota",
            None,
            {"backfillUserfacts": StringCollection(backfill_userfacts)},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
