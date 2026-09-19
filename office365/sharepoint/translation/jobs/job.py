from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.entity import Entity


class TranslationJob(Entity):
    """The TranslationJob type is used to create new translation jobs."""

    def __init__(self, context, target_language: str):
        super().__init__(
            context, ServiceOperationPath("SP.Translation.TranslationJob", {"targetLanguage": target_language})
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

    @property
    def job_id(self) -> Optional[UUID]:
        """Gets the JobId property"""
        return self.properties.get("JobId", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def output_save_behavior(self) -> Optional[int]:
        """Gets the OutputSaveBehavior property"""
        return self.properties.get("OutputSaveBehavior", None)

    def translate_file(self, input_file: str, output_file: str) -> ClientResult[str]:
        """TranslateFile operation.

        Args:
            input_file (str): inputFile parameter
            output_file (str): outputFile parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self, "TranslateFile", None, {"inputFile": input_file, "outputFile": output_file}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def translate_folder(self, input_folder: str, output_folder: str, recursion: bool) -> ClientResult[str]:
        """TranslateFolder operation.

        Args:
            input_folder (str): inputFolder parameter
            output_folder (str): outputFolder parameter
            recursion (bool): recursion parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "TranslateFolder",
            None,
            {"inputFolder": input_folder, "outputFolder": output_folder, "recursion": recursion},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def translate_library(self, input_library: str, output_library: str) -> ClientResult[str]:
        """TranslateLibrary operation.

        Args:
            input_library (str): inputLibrary parameter
            output_library (str): outputLibrary parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "TranslateLibrary",
            None,
            {"inputLibrary": input_library, "outputLibrary": output_library},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
