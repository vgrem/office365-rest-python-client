from __future__ import annotations

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.news_distribution_settings import NewsDistributionSettings


class ContentDistributionController(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.ContentDistributionController"

    def get_news_distribution_settings(self) -> ClientResult[NewsDistributionSettings]:
        """GetNewsDistributionSettings operation."""
        return_type = ClientResult(self.context, NewsDistributionSettings())
        qry = FunctionQuery(self, "GetNewsDistributionSettings", [], return_type)
        self.context.add_query(qry)
        return return_type

    def set_news_distribution_settings(self, community_id: str) -> Self:
        """SetNewsDistributionSettings operation.

        Args:
            community_id (str): communityId parameter
        """
        qry = ServiceOperationQuery(self, "SetNewsDistributionSettings", None, {"communityId": community_id}, None, None)
        self.context.add_query(qry)
        return self
