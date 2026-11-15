from __future__ import annotations

from typing import Optional

from office365.communications.operations.comms import CommsOperation
from office365.runtime.types.odata_property import odata


class RecordOperation(CommsOperation):
    @odata(name="recordingAccessToken")
    @property
    def recording_access_token(self) -> Optional[str]:
        """Gets the recordingAccessToken property"""
        return self.properties.get("recordingAccessToken", None)

    @odata(name="recordingLocation")
    @property
    def recording_location(self) -> Optional[str]:
        """Gets the recordingLocation property"""
        return self.properties.get("recordingLocation", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RecordOperation"
