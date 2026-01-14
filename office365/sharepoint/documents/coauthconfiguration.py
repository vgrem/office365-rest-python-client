from datetime import datetime

from office365.runtime.client_value import ClientValue


class CoAuthConfiguration(ClientValue):
    def __init__(
        self,
        source_session_id: str = None,
        update_date: datetime = datetime.min,
        update_reason: int = None,
    ):
        self.source_session_id = source_session_id
        self.update_date = update_date
        self.update_reason = update_reason
