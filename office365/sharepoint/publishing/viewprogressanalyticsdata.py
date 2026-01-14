from office365.runtime.client_value import ClientValue


class ViewProgressAnalyticsData(ClientValue):
    def __init__(self, percentage_viewed: int = None):
        self.PercentageViewed = percentage_viewed

    @property
    def entity_type_name(self):
        return "SP.Publishing.ViewProgressAnalyticsData"
