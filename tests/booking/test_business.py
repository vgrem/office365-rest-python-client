"""Tests for Microsoft Graph Booking API."""

from typing import Optional

from office365.booking.business.business import BookingBusiness
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestBusiness(GraphDelegatedTestCase):
    """Tests for Booking businesses."""

    business: Optional[BookingBusiness] = None

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        "BookingsAppointment.ReadWrite.All",
        or_roles=["Global Administrator"],
    )
    def test1_list_booking_business(self):
        """List all booking businesses."""
        result = self.client.solutions.booking_businesses.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Bookings.Manage.All", or_roles=["Global Administrator"])
    def test2_create_booking_business(self):
        """Create a new booking business."""
        result = self.client.solutions.booking_businesses.add("Fourth Coffee").execute_query()
        self.assertIsNotNone(result.resource_path)
        TestBusiness.business = result

    @requires_delegated(
        "Bookings.Read.All",
        "Bookings.Manage.All",
        "Bookings.ReadWrite.All",
        "BookingsAppointment.ReadWrite.All",
        or_roles=["Global Administrator"],
    )
    def test3_ensure_created(self):
        """Verify the booking business was created."""
        assert TestBusiness.business is not None
        result = TestBusiness.business.get().execute_query_retry()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Bookings.Manage.All", or_roles=["Global Administrator"])
    def test4_publish(self):
        """Publish the booking business."""
        assert TestBusiness.business is not None
        result = TestBusiness.business.publish().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Bookings.Manage.All", or_roles=["Global Administrator"])
    def test5_delete_booking_business(self):
        """Delete the booking business."""
        assert TestBusiness.business is not None
        TestBusiness.business.delete_object().execute_query_retry()
