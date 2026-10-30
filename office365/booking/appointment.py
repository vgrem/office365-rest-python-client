from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.booking.customers.informationbase import BookingCustomerInformationBase
from office365.booking.pricetype import BookingPriceType
from office365.booking.reminder import BookingReminder
from office365.entity import Entity
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.mail.location import Location
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.runtime.types.duration import timedelta


class BookingAppointment(Entity):
    """
    Represents a business in Microsoft Bookings. This is the top level object in the Microsoft Bookings API.
    It contains business information and related business objects such as appointments, customers, services,
    and staff members.
    """

    @odata(name="additionalInformation")
    @property
    def additional_information(self) -> Optional[str]:
        """Gets the additionalInformation property"""
        return self.properties.get("additionalInformation", None)

    @odata(name="anonymousJoinWebUrl")
    @property
    def anonymous_join_web_url(self) -> Optional[str]:
        """Gets the anonymousJoinWebUrl property"""
        return self.properties.get("anonymousJoinWebUrl", None)

    @odata(name="appointmentLabel")
    @property
    def appointment_label(self) -> Optional[str]:
        """Gets the appointmentLabel property"""
        return self.properties.get("appointmentLabel", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="customerEmailAddress")
    @property
    def customer_email_address(self) -> Optional[str]:
        """Gets the customerEmailAddress property"""
        return self.properties.get("customerEmailAddress", None)

    @odata(name="customerName")
    @property
    def customer_name(self) -> Optional[str]:
        """Gets the customerName property"""
        return self.properties.get("customerName", None)

    @odata(name="customerNotes")
    @property
    def customer_notes(self) -> Optional[str]:
        """Gets the customerNotes property"""
        return self.properties.get("customerNotes", None)

    @odata(name="customerPhone")
    @property
    def customer_phone(self) -> Optional[str]:
        """Gets the customerPhone property"""
        return self.properties.get("customerPhone", None)

    @odata(name="customers")
    @property
    def customers(self) -> ClientValueCollection[BookingCustomerInformationBase]:
        """Gets the customers property"""
        return self.properties.get(
            "customers", ClientValueCollection[BookingCustomerInformationBase](BookingCustomerInformationBase)
        )

    @odata(name="customerTimeZone")
    @property
    def customer_time_zone(self) -> Optional[str]:
        """Gets the customerTimeZone property"""
        return self.properties.get("customerTimeZone", None)

    @odata(name="duration", readonly=True)
    @property
    def duration(self) -> Optional[timedelta]:
        """Gets the duration property"""
        return self.properties.get("duration", None)

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> DateTimeTimeZone:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", DateTimeTimeZone())

    @odata(name="filledAttendeesCount", readonly=True)
    @property
    def filled_attendees_count(self) -> Optional[int]:
        """Gets the filledAttendeesCount property"""
        return self.properties.get("filledAttendeesCount", None)

    @odata(name="isCustomerAllowedToManageBooking")
    @property
    def is_customer_allowed_to_manage_booking(self) -> Optional[bool]:
        """Gets the isCustomerAllowedToManageBooking property"""
        return self.properties.get("isCustomerAllowedToManageBooking", None)

    @odata(name="isLocationOnline")
    @property
    def is_location_online(self) -> Optional[bool]:
        """Gets the isLocationOnline property"""
        return self.properties.get("isLocationOnline", None)

    @odata(name="joinWebUrl")
    @property
    def join_web_url(self) -> Optional[str]:
        """Gets the joinWebUrl property"""
        return self.properties.get("joinWebUrl", None)

    @odata(name="lastUpdatedDateTime")
    @property
    def last_updated_date_time(self) -> Optional[datetime]:
        """Gets the lastUpdatedDateTime property"""
        return self.properties.get("lastUpdatedDateTime", datetime.min)

    @odata(name="maximumAttendeesCount")
    @property
    def maximum_attendees_count(self) -> Optional[int]:
        """Gets the maximumAttendeesCount property"""
        return self.properties.get("maximumAttendeesCount", None)

    @odata(name="optOutOfCustomerEmail")
    @property
    def opt_out_of_customer_email(self) -> Optional[bool]:
        """Gets the optOutOfCustomerEmail property"""
        return self.properties.get("optOutOfCustomerEmail", None)

    @odata(name="postBuffer")
    @property
    def post_buffer(self) -> Optional[timedelta]:
        """Gets the postBuffer property"""
        return self.properties.get("postBuffer", None)

    @odata(name="preBuffer")
    @property
    def pre_buffer(self) -> Optional[timedelta]:
        """Gets the preBuffer property"""
        return self.properties.get("preBuffer", None)

    @odata(name="price")
    @property
    def price(self) -> Optional[float]:
        """Gets the price property"""
        return self.properties.get("price", None)

    @odata(name="priceType")
    @property
    def price_type(self) -> BookingPriceType:
        """Gets the priceType property"""
        return self.properties.get("priceType", BookingPriceType.undefined)

    @odata(name="reminders")
    @property
    def reminders(self) -> ClientValueCollection[BookingReminder]:
        """Gets the reminders property"""
        return self.properties.get("reminders", ClientValueCollection[BookingReminder](BookingReminder))

    @odata(name="selfServiceAppointmentId")
    @property
    def self_service_appointment_id(self) -> Optional[str]:
        """Gets the selfServiceAppointmentId property"""
        return self.properties.get("selfServiceAppointmentId", None)

    @odata(name="serviceId")
    @property
    def service_id(self) -> Optional[str]:
        """Gets the serviceId property"""
        return self.properties.get("serviceId", None)

    @odata(name="serviceLocation")
    @property
    def service_location(self) -> Location:
        """Gets the serviceLocation property"""
        return self.properties.get("serviceLocation", Location())

    @odata(name="serviceName")
    @property
    def service_name(self) -> Optional[str]:
        """Gets the serviceName property"""
        return self.properties.get("serviceName", None)

    @odata(name="serviceNotes")
    @property
    def service_notes(self) -> Optional[str]:
        """Gets the serviceNotes property"""
        return self.properties.get("serviceNotes", None)

    @odata(name="smsNotificationsEnabled")
    @property
    def sms_notifications_enabled(self) -> Optional[bool]:
        """Gets the smsNotificationsEnabled property"""
        return self.properties.get("smsNotificationsEnabled", None)

    @odata(name="staffMemberIds")
    @property
    def staff_member_ids(self) -> StringCollection:
        """Gets the staffMemberIds property"""
        return self.properties.get("staffMemberIds", StringCollection())

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> DateTimeTimeZone:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", DateTimeTimeZone())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BookingAppointment"
