from office365.runtime.client_value import ClientValue


class GridInitInfoType(ClientValue):
    def __init__(
        self,
        controller_id: str = None,
        grid_serializer: str = None,
        js_init_obj: str = None,
    ):
        self.controller_id = controller_id
        self.grid_serializer = grid_serializer
        self.js_init_obj = js_init_obj
