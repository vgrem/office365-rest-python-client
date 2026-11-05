from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class DirectorySessionData(ClientValue):
    ClientType: Optional[str] = None
    SessionOptions: Optional[str] = None

    @property
    def entity_type_name(self) -> str:
        return "SP.Directory.Provider.DirectorySessionData"
