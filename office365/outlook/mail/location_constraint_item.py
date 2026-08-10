from office365.outlook.mail.location import Location


class LocationConstraintItem(Location):
    resolveAvailability: bool | None = None
    "The conditions stated by a client for the location of a meeting."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LocationConstraintItem"
