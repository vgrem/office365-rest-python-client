from __future__ import annotations

from dataclasses import dataclass

from office365.booking.pageaccesscontrol import BookingPageAccessControl
from office365.runtime.client_value import ClientValue


@dataclass
class BookingPageSettings(ClientValue):
    accessControl: BookingPageAccessControl | None = None
    bookingPageColorCode: str | None = None
    businessTimeZone: str | None = None
    customerConsentMessage: str | None = None
    enforceOneTimePassword: bool | None = None
    isBusinessLogoDisplayEnabled: bool | None = None
    isCustomerConsentEnabled: bool | None = None
    isSearchEngineIndexabilityDisabled: bool | None = None
    isTimeSlotTimeZoneSetToBusinessTimeZone: bool | None = None
    privacyPolicyWebUrl: str | None = None
    termsAndConditionsWebUrl: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingPageSettings"
