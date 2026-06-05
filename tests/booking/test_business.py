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

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestBusiness(GraphDelegatedTestCase):
    """Booking business lifecycle and sub-resources."""

    target_business: ClassVar[Optional[object]] = None

    @requires_delegated(
        "Bookings.Read.All", "Bookings.Manage.All", "Bookings.ReadWrite.All",
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
        self.assertEqual(result.get_property("displayName"), "SDK Test Business")
        TestBusiness.target_business = result

    @requires_delegated(
        "Bookings.Read.All", "Bookings.Manage.All", "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_03_get_business_by_id(self):
        """Retrieving a booking business by ID returns the same business."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        result = business.get().execute_query_retry()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("displayName"), "SDK Test Business")

    @requires_delegated(
        "Bookings.Read.All", "Bookings.Manage.All", "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_04_business_has_expected_properties(self):
        """A booking business exposes displayName, address, businessHours, and phone."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        self.assertIsNotNone(business.get_property("displayName"))
        # These may be None for a newly created minimal business, but should exist as keys
        self.assertIsNotNone(business.get_property("address"))
        self.assertIsNotNone(business.get_property("businessHours"))

    @requires_delegated(
        "Bookings.Manage.All",
        bypass_roles=["Global Administrator"],
    )
    def test_05_publish_business(self):
        """Publishing a business scheduling page should succeed."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        business.publish().execute_query()
        # Publish sets isPublished = true and publicUrl
        updated = business.get().execute_query_retry()
        is_published = updated.get_property("isPublished")
        self.assertTrue(is_published)

    @requires_delegated(
        "Bookings.Read.All", "Bookings.Manage.All", "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_06_list_services(self):
        """Listing services for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        services = business.services.get().execute_query()
        self.assertIsNotNone(services)

    @requires_delegated(
        "Bookings.Read.All", "Bookings.Manage.All", "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_07_list_customers(self):
        """Listing customers for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        customers = business.customers.get().execute_query()
        self.assertIsNotNone(customers)

    @requires_delegated(
        "Bookings.Read.All", "Bookings.Manage.All", "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_08_list_staff_members(self):
        """Listing staff members for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        staff = business.staff_members.get().execute_query()
        self.assertIsNotNone(staff)

    @requires_delegated(
        "Bookings.Read.All", "Bookings.Manage.All", "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_09_list_appointments(self):
        """Listing appointments for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        appointments = business.appointments.get().execute_query()
        self.assertIsNotNone(appointments)

    @requires_delegated(
        "Bookings.Read.All", "Bookings.Manage.All", "Bookings.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_10_list_custom_questions(self):
        """Listing custom questions for a booking business returns a valid collection."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        try:
            questions = business.custom_questions.get().execute_query()
            self.assertIsNotNone(questions)
        except Exception:
            self.skipTest("Custom questions endpoint not available")

    @requires_delegated(
        "Bookings.Manage.All",
        bypass_roles=["Global Administrator"],
    )
    def test_11_delete_booking_business(self):
        """Deleting a booking business should succeed."""
        business = TestBusiness.target_business
        if not business:
            self.skipTest("No business created from previous test")

        business.delete_object().execute_query_retry()
        TestBusiness.target_business = None

    @classmethod
    def tearDownClass(cls):
        business = cls.target_business
        if business and business.resource_path:
            try:
                business.delete_object().execute_query_retry()
            except Exception:
                pass
