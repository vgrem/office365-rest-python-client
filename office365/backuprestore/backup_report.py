from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery

if TYPE_CHECKING:
    from office365.backuprestore.backup_policy_report import BackupPolicyReport


class BackupReport(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BackupReport"

    def get_statistics_by_policy(self, policy_id: str) -> ClientResult[BackupPolicyReport]:
        """getStatisticsByPolicy operation.

        Args:
            policy_id (str):
                policyId parameter
        """
        from office365.backuprestore.backup_policy_report import BackupPolicyReport

        return_type = ClientResult(self.context, BackupPolicyReport())
        qry = FunctionQuery(self, "getStatisticsByPolicy", {"policyId": policy_id}, return_type)
        self.context.add_query(qry)
        return return_type
