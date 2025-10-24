from enum import Enum


class OnenotePatchInsertPosition(Enum):
    After = "0"
    Before = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnenotePatchInsertPosition"
