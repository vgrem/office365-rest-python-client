from office365.runtime.client_value import ClientValue


class FieldGeolocationValue(ClientValue):
    def __init__(
        self,
        latitude: float,
        longitude: float,
        altitude: float = None,
        measure: float = None,
    ):
        """
        Specifies altitude, latitude, longitude and measure values for FieldGeolocation (section 3.2.5.185).<191>

        :param float latitude: Specifies the latitude value for Geolocation field.
        :param float longitude: Specifies the longitude value for Geolocation field.
        :param float altitude: Specifies the altitude value for Geolocation field. It is a user defined value

        """
        super().__init__()
        self.Latitude = latitude
        self.Longitude = longitude
        self.Altitude = altitude
        self.Measure = measure

    @property
    def entity_type_name(self):
        return "SP.FieldGeolocationValue"
