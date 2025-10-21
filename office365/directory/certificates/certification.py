from datetime import datetime

from office365.runtime.client_value import ClientValue


class Certification(ClientValue):
    """Represents the certification details of an application."""

    def __init__(
        self,
        certification_details_url: str = None,
        certification_expiration_date_time: datetime = None,
        is_certified_by_microsoft: bool = None,
        is_publisher_attested: bool = None,
        last_certification_date_time: datetime = None,
    ):
        """
        :param str certification_details_url:
        """
        self.certificationDetailsUrl = certification_details_url
        self.certificationExpirationDateTime = certification_expiration_date_time
        self.isCertifiedByMicrosoft = is_certified_by_microsoft
        self.isPublisherAttested = is_publisher_attested
        self.lastCertificationDateTime = last_certification_date_time

    @property
    def entity_type_name(self):
        return "microsoft.graph.Certification"
