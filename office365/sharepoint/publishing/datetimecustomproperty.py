from office365.runtime.client_value import ClientValue


class DateTimeCustomProperty(ClientValue):

    def __init__(self, custom_property_name: str = None):
        self.CustomPropertyName = custom_property_name
