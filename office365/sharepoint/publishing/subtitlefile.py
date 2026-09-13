from typing import Optional

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class SubtitleFile(Entity):
    @property
    def language(self) -> Optional[str]:
        """Gets the Language property"""
        return self.properties.get("Language", None)

    @property
    def native_language_name(self) -> Optional[str]:
        """Gets the NativeLanguageName property"""
        return self.properties.get("NativeLanguageName", None)

    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.SubtitleFile"

    def add(self, language: str, extension: str, stream: bytes) -> Self:
        """Add operation.

        Args:
            language (str): language parameter
            extension (str): extension parameter
            stream (bytes): stream parameter
        """
        qry = ServiceOperationQuery(
            self, "Add", None, {"language": language, "extension": extension, "stream": stream}, None, None
        )
        self.context.add_query(qry)
        return self

    def get_subtitle_file(self, name: str) -> ClientResult[bytes]:
        """GetSubtitleFile operation.

        Args:
            name (str): name parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(self, "GetSubtitleFile", [name], return_type, return_raw_content=True)
        self.context.add_query(qry)
        return return_type

    def remove(self, name: str) -> Self:
        """Remove operation.

        Args:
            name (str): name parameter
        """
        qry = ServiceOperationQuery(self, "Remove", None, {"name": name}, None, None)
        self.context.add_query(qry)
        return self
