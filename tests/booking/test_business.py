"""Bookings — businesses, services, appointments, customers, and staff.

Tests cover:
  - Listing booking businesses
  - Creating a booking business with display name
  - Retrieving a business by ID and verifying properties
  - Publishing a business scheduling page
  - Listing services, appointments, customers, staff_members
  - Staff availability queries
  - Deleting a business
  - Property assertions (displayName, businessHours, address)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.booking.business.business import BookingBusiness
from office365.runtime.client_request_exception import ClientRequestException
from tests.decorators import requires_call, requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class BookingCase(GraphDelegatedTestCase):
    """A suite that needs a Bookings mailbox, which this tenant was never given.

    Measured: creating a business succeeds and answers an object with an id, but reading it
    back - and its services, staff, customers, and publish - answers ``('NotFound', 'Bookings
    mailbox was not found.')``, while deleting it answers ``Invalid authority. List Staff
    members failed. ... User not found in directory``: the mailbox that would answer both
    does not exist. Two spellings, one absence, so both skip.
    """

    #: Both measured because the deletion path resolves the mailbox through the directory
    #: rather than through the Bookings service.
    _NO_MAILBOX = ("Bookings mailbox was not found", "List Staff members failed")

    def call(self, request):
        """Execute ``request``, or skip when this tenant has no Bookings mailbox."""
        try:
            return request.execute_query()
        except ClientRequestException as error:
            if not any(marker in str(error) for marker in self._NO_MAILBOX):
                raise
            self.skipTest(f"this tenant has no Bookings mailbox: {error}")


class TestBusiness(BookingCase):
    """Booking business lifecycle and sub-resources."""

    target_business: ClassVar[Optional[BookingBusiness]] = None

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_01_list_booking_businesses(self):
        """Listing all booking businesses returns a valid collection."""
        result = self.client.solutions.booking_businesses.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Bookings.Manage.All",
        bypass_roles=["Global Administrator"],
    )
    def test_02_create_booking_business(self):
        """Creating a booking business with a display name should succeed."""
        result = self.client.solutions.booking_businesses.add("SDK Test Business").execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.display_name, "SDK Test Business")
        TestBusiness.target_business = result

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_03_get_business_by_id(self):
        """Retrieving a booking business by ID returns the same business."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        result = self.call(business.get())
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.display_name, "SDK Test Business")

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_04_business_has_expected_properties(self):
        """A booking business exposes displayName, address, businessHours, and phone."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        self.assertIsNotNone(business.display_name)
        # These may be None for a newly created minimal business, but should exist as keys
        self.assertIsNotNone(business.address)
        self.assertIsNotNone(business.business_hours)

    @requires_call(BookingBusiness.publish, flow="delegated", bypass_roles=["Global Administrator"])
    def test_05_publish_business(self):
        """Publishing a business scheduling page should succeed."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        self.call(business.publish())
        # Publish sets isPublished = true and publicUrl
        updated = self.call(business.get())
        is_published = updated.get_property("isPublished")
        self.assertTrue(is_published)

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_06_list_services(self):
        """Listing services for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        services = self.call(business.services.get())
        self.assertIsNotNone(services)

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_07_list_customers(self):
        """Listing customers for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        customers = self.call(business.customers.get())
        self.assertIsNotNone(customers)

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_08_list_staff_members(self):
        """Listing staff members for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        staff = self.call(business.staff_members.get())
        self.assertIsNotNone(staff)

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_09_list_appointments(self):
        """Listing appointments for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        appointments = self.call(business.appointments.get())
        self.assertIsNotNone(appointments)

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_10_list_custom_questions(self):
        """Listing custom questions for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        questions = self.call(business.custom_questions.get())
        self.assertIsNotNone(questions)

    @requires_delegated(
        "Bookings.Manage.All",
        bypass_roles=["Global Administrator"],
    )
    def test_11_delete_booking_business(self):
        """Deleting a booking business should succeed."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        self.call(business.delete_object())
        TestBusiness.target_business = None

    @classmethod
    def tearDownClass(cls):
        business = cls.target_business
        if business and business.resource_path:
            try:
                business.delete_object().execute_query_retry()
            except ClientRequestException:
                pass
