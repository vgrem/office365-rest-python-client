from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext
    from office365.sharepoint.spark.category import SparkCategory
    from office365.sharepoint.spark.category_similarity_result import SparkCategorySimilarityResult
    from office365.sharepoint.spark.embedding_result import SparkEmbeddingResult


class SPARK(Entity):
    @staticmethod
    def get_category_similarity(
        context: ClientContext, text: str, scenario_id: str, categories: ClientValueCollection[SparkCategory]
    ) -> ClientResult[SparkCategorySimilarityResult]:
        """GetCategorySimilarity operation.

        Args:
            text (str):
                text parameter
            scenario_id (str):
                scenarioId parameter
            categories (ClientValueCollection[SparkCategory]):
                categories parameter
        """
        from office365.sharepoint.spark.category_similarity_result import SparkCategorySimilarityResult

        return_type = ClientResult(context, SparkCategorySimilarityResult())
        qry = ServiceOperationQuery(
            SPARK(context),
            "GetCategorySimilarity",
            None,
            {"text": text, "scenarioId": scenario_id, "categories": categories},
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_embedding(context: ClientContext, texts: list[str], scenario_id: str) -> ClientResult[SparkEmbeddingResult]:
        """GetEmbedding operation.

        Args:
            texts (list[str]):
                texts parameter
            scenario_id (str):
                scenarioId parameter
        """
        from office365.sharepoint.spark.embedding_result import SparkEmbeddingResult

        return_type = ClientResult(context, SparkEmbeddingResult())
        qry = ServiceOperationQuery(
            SPARK(context),
            "GetEmbedding",
            None,
            {"texts": StringCollection(texts), "scenarioId": scenario_id},
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_summarization(context: ClientContext, texts: list[str]) -> ClientResult[str]:
        """GetSummarization operation.

        Args:
            texts (list[str]):
                texts parameter
        """

        return_type = ClientResult(context, str())
        qry = ServiceOperationQuery(
            SPARK(context), "GetSummarization", None, {"texts": StringCollection(texts)}, None, return_type, True
        )
        context.add_query(qry)
        return return_type
