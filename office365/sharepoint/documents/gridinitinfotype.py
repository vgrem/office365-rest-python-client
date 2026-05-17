from typing import Optional

from office365.runtime.client_value import ClientValue


class GridInitInfoType(ClientValue):
    def __init__(
        self,
        controller_id: Optional[str] = None,
        grid_serializer: Optional[str] = None,
        js_init_obj: Optional[str] = None,
    ):
        self.controller_id = controller_id
        self.grid_serializer = grid_serializer
        self.js_init_obj = js_init_obj
