from office365.booking.pageaccesscontrol import BookingPageAccessControl
from office365.runtime.client_value import ClientValue


class BookingPageSettings(ClientValue):

    def __init__(
        self,
        access_control: BookingPageAccessControl = BookingPageAccessControl.none,
        booking_page_color_code: str = None,
        business_time_zone: str = None,
        customer_consent_message: str = None,
        enforce_one_time_password: bool = None,
        is_business_logo_display_enabled: bool = None,
        is_customer_consent_enabled: bool = None,
        is_search_engine_indexability_disabled: bool = None,
        is_time_slot_time_zone_set_to_business_time_zone: bool = None,
        privacy_policy_web_url: str = None,
        terms_and_conditions_web_url: str = None,
    ):
        self.accessControl = access_control
        self.bookingPageColorCode = booking_page_color_code
        self.businessTimeZone = business_time_zone
        self.customerConsentMessage = customer_consent_message
        self.enforceOneTimePassword = enforce_one_time_password
        self.isBusinessLogoDisplayEnabled = is_business_logo_display_enabled
        self.isCustomerConsentEnabled = is_customer_consent_enabled
        self.isSearchEngineIndexabilityDisabled = is_search_engine_indexability_disabled
        self.isTimeSlotTimeZoneSetToBusinessTimeZone = is_time_slot_time_zone_set_to_business_time_zone
        self.privacyPolicyWebUrl = privacy_policy_web_url
        self.termsAndConditionsWebUrl = terms_and_conditions_web_url

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingPageSettings"
