from office365.runtime.client_value import ClientValue


class PageImpressionClient(ClientValue):
    def __init__(
        self,
        base_page_correlation_id: str = None,
        client_id_to_click_info_map: dict = None,
    ):
        self.BasePageCorrelationId = base_page_correlation_id
        self.ClientIdToClickInfoMap = client_id_to_click_info_map

    @property
    def entity_type_name(self):
        return "SP.PageInstrumentation.PageImpressionClient"
