from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ConvertIdResult(ClientValue):
    """The result of an ID format conversion performed by the translateExchangeIds function.

    Fields:
        sourceId (str | None): The identifier that was converted. This value is the original, un-converted identifier.
        targetId (str | None): The converted identifier. This value is not present if the conversion failed.
    """

    sourceId: str | None = None
    targetId: str | None = None
