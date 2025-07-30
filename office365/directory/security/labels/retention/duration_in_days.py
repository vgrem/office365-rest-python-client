from office365.directory.security.labels.retention.duration import RetentionDuration


class RetentionDurationInDays(RetentionDuration):
    """"""

    def __init__(self, days: int = None):
        super().__init__()
        self.days = days

    @property
    def entity_type_name(self):
        return "microsoft.graph.security.retentionDurationInDays"
