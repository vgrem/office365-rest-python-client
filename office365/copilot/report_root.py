from __future__ import annotations

from office365.entity import Entity
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery


class CopilotReportRoot(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopilotReportRoot"

    def get_microsoft365_copilot_usage_user_detail(self, period: str, version: str) -> ClientResult[bytes]:
        """getMicrosoft365CopilotUsageUserDetail operation.

        Args:
            period (str):
                period parameter
            version (str):
                version parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self,
            "getMicrosoft365CopilotUsageUserDetail",
            {"period": period, "version": version},
            return_type,
            return_raw_content=True,
        )
        self.context.add_query(qry)
        return return_type

    def get_microsoft365_copilot_user_count_summary(self, period: str, version: str) -> ClientResult[bytes]:
        """getMicrosoft365CopilotUserCountSummary operation.

        Args:
            period (str):
                period parameter
            version (str):
                version parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self,
            "getMicrosoft365CopilotUserCountSummary",
            {"period": period, "version": version},
            return_type,
            return_raw_content=True,
        )
        self.context.add_query(qry)
        return return_type

    def get_microsoft365_copilot_user_count_trend(self, period: str, version: str) -> ClientResult[bytes]:
        """getMicrosoft365CopilotUserCountTrend operation.

        Args:
            period (str):
                period parameter
            version (str):
                version parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self,
            "getMicrosoft365CopilotUserCountTrend",
            {"period": period, "version": version},
            return_type,
            return_raw_content=True,
        )
        self.context.add_query(qry)
        return return_type
