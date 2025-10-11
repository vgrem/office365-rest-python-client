from office365.runtime.client_value import ClientValue


class AlertHistoryState(ClientValue):
    """Stores changes made to alerts."""

    def __init__(self, app_id: str = None, assigned_to: str = None, comments: list[str] = None) -> None:
        self.appId = app_id
        self.assignedTo = assigned_to
        self.comments = comments
