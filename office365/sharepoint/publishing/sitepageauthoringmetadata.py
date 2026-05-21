from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SitePageAuthoringMetadata(ClientValue):
    ClientOperation: Optional[int] = None
    FluidContainerCustomId: Optional[str] = None
    IsSingleUserSession: Optional[bool] = None
    RestoredFrom: Optional[str] = None
    RestoreTo: Optional[str] = None
    SequenceId: Optional[int] = None
    SessionId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageAuthoringMetadata"
