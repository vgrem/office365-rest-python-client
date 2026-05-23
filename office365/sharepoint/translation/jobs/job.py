from __future__ import annotations

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.entity import Entity


class TranslationJob(Entity):
    """The TranslationJob type is used to create new translation jobs."""

    def __init__(self, context, target_language: str):
        super().__init__(
            context,
            ServiceOperationPath("SP.Translation.TranslationJob", {"targetLanguage": target_language}),
        )

    @staticmethod
    def is_service_enabled(context: ClientContext, target_language: str) -> ClientResult[bool]:
        """Determines if translation to or from a given language is supported.

        Args:
            context: The SharePoint client context.
            target_language: A valid language tag as specified in RFC1766.
        """
        return_type = ClientResult(context, bool())
        binding_type = TranslationJob(context, target_language)
        qry = ServiceOperationQuery(binding_type, "IsServiceEnabled", None, None, None, return_type)
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self) -> str:
        return "SP.Translation.TranslationJob"
