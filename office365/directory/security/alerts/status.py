class AlertStatus:
    """"""

    unknown = "0"
    newAlert = "1"
    inProgress = "2"
    resolved = "3"
    dismissed = "4"
    unknownFutureValue = "127"
    new = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AlertStatus"
