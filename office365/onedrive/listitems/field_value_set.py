from office365.onedrive.base_item import BaseItem


class FieldValueSet(BaseItem):
    """Represents the column values in a listItem resource."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.fieldValueSet"
