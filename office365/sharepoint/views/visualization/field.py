from office365.runtime.client_value import ClientValue


class VisualizationField(ClientValue):
    """Contains CSS properties relating to how an individual field is layed out relative to it's container."""

    def __init__(self, internal_name: str = None, style: str = None):
        """
        :param str internal_name: A Property which will specify which set of sub-elements to apply this set of
            CSS properties on.
        :param str style: CSS properties in serialized JSON format.
        """
        self.InternalName = internal_name
        self.Style = style
