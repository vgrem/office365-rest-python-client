"""
Microsoft Bookings — manage businesses, services, appointments,
staff, and customers.

Bookings is Microsoft's appointment scheduling solution. This example
covers the full lifecycle:
  - List booking businesses
  - List services for a business
  - Get staff availability
  - Create an appointment
  - List customers

Requires delegated permission ``Bookings.ReadWrite.All``,
``BookingsAppointment.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/resources/booking-api-overview
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    # -- Step 1: list booking businesses --
    businesses = client.solutions.booking_businesses.get().execute_query()
    print(f"Booking businesses: {len(businesses)}\n")

    for b in businesses:
        address = b.address
        display = b.display_name or "(unnamed)"
        city = address.city if address else "?"
        print(f"  {display:40s}  city={city}")

    if not businesses:
        print("  (no booking businesses — create one first at https://outlook.office.com/bookings)")
        print()
        # Create a sample business (commented)
        # from office365.booking.business.collection import BookingBusinessCollection
        # new_biz = client.solutions.booking_businesses.add(displayName="Demo Consulting").execute_query()
        # print(f"Created: {new_biz.display_name}")
        return

    biz = businesses[0]
    print(f"\nInspecting: {biz.display_name}")
    print("  Business hours:")
    if biz.business_hours and biz.business_hours.value:
        for wh in biz.business_hours.value:
            print(f"    {wh.properties.get('day', '?'):10s}  {wh.properties.get('timeSlots', [])}")

    # -- Step 2: list services --
    services = biz.services.get().execute_query()
    print(f"\n  Services ({len(services)}):")
    for s in services:
        display = s.properties.get("displayName", "?")
        duration = s.properties.get("duration", "?")
        price = s.properties.get("defaultPrice", "?")
        currency = s.properties.get("defaultPriceType", "?")
        print(f"    {display:35s}  duration={duration}  price={price} {currency}")

    # -- Step 3: get staff availability --
    print("\n  Getting staff availability for next 7 days...")
    staff = biz.staff_members.get().execute_query()
    print(f"  Staff members: {len(staff)}")
    for s in staff[:3]:
        name = s.properties.get("displayName", "?")
        email = s.properties.get("emailAddress", "?")
        availability = biz.get_staff_availability(
            staff_ids=[s.id],
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc) + timedelta(days=7),
        ).execute_query()
        print(f"    {name:25s}  {email:30s}")

    # -- Step 4: create an appointment --
    if services:
        service = services[0]
        now = datetime.now(timezone.utc)
        start = now + timedelta(days=1, hours=9)
        end = start + timedelta(hours=1)

        appointment = biz.appointments.add(
            serviceId=service.id,
            serviceName=service.properties.get("displayName", "Consultation"),
            startDateTime={"dateTime": start.isoformat(), "timeZone": "UTC"},
            endDateTime={"dateTime": end.isoformat(), "timeZone": "UTC"},
            customerEmail="client@example.com",
            customerName="John Doe",
            customerPhone="+1 555 123 4567",
            additionalInformation="Initial consultation booking via API",
        ).execute_query()
        print(f"\n  ✓ Appointment created: {appointment.id}")

    # -- Step 5: list customers --
    customers = biz.customers.get().execute_query()
    print(f"\n  Customers: {len(customers)}")
    for c in customers:
        name = c.properties.get("displayName", "?")
        email = c.properties.get("emailAddress", "?")
        print(f"    {name:30s}  {email}")


if __name__ == "__main__":
    main()
