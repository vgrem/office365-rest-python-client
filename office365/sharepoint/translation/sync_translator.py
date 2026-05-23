from __future__ import annotations

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.translation.item_info import TranslationItemInfo


class SyncTranslator(Entity):
    """The SyncTranslator type is used to submit immediate translation jobs to the protocol server.

    Note: The Machine Translations Service API will no longer be supported as of the end of July 2022.
    https://go.microsoft.com/fwlink/?linkid=2187153
    """

    def __init__(self, context, target_language: str):
        super().__init__(
            context,
            ServiceOperationPath("SP.Translation.SyncTranslator", {"targetLanguage": target_language}),
        )

    def translate(self, input_file: str, output_file: str) -> ClientResult[TranslationItemInfo]:
        """Submits an immediate translation job to the protocol server.

        Args:
            input_file: Full or relative path to the file to be translated.
            output_file: Full or relative path where the translated document will be stored.
        """
        payload = {"inputFile": input_file, "outputFile": output_file}
        return_type = ClientResult(self.context, TranslationItemInfo())
        qry = ServiceOperationQuery(self, "Translate", None, payload)
        self.context.add_query(qry)
        return return_type

    @property
    def output_save_behavior(self) -> int | None:
        """Determines the behavior when the output file already exists during translation.

        If not set, AppendIfPossible behavior is used.
        """
        return self.properties.get("OutputSaveBehavior", None)

    @property
    def entity_type_name(self) -> str:
        return "SP.Translation.SyncTranslator"
