from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ResultInfo(ClientValue):
    code: int | None = None
    message: str | None = None
    subcode: int | None = None
    "\n    This contains success and failure specific result information.\n\n    The code specifies if the result is a generic success or failure. If the code is 2xx it's a success,\n    if it's a 4xx it's a client error, and if it's 5xx, it's a server error.\n\n    The sub-codes provide supplementary information related to the type of success or failure\n    (e.g. a call transfer was successful)\n    "

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResultInfo"
