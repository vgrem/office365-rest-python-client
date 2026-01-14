from office365.runtime.client_value import ClientValue


class AutoLabellingWorkInformation(ClientValue):
    def __init__(
        self,
        routing_hint: str = None,
        scale_unit_id: str = None,
        watermark: str = None,
        work_item_type: int = None,
    ):
        self.routing_hint = routing_hint
        self.scale_unit_id = scale_unit_id
        self.watermark = watermark
        self.work_item_type = work_item_type
