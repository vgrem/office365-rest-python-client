"""
Microsoft Bookings — manage businesses, services, appointments, staff, and customers.

Bookings is Microsoft's appointment scheduling solution. This example covers the
full lifecycle with subcommands:

  list                  List booking businesses
  show                  Show business details (hours, services, staff, customers)
  availability          Staff availability for the next N days
  add-appointment       Book an appointment with a customer
  add-customer          Add a customer
  create                Create a booking business
  publish               Publish the scheduling page

Requires delegated permission ``Bookings.ReadWrite.All`` and
``BookingsAppointment.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/resources/booking-api-overview
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from typing import Optional

from office365.booking.business.business import BookingBusiness
from office365.graph_client import GraphClient
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from tests.settings import client_id, client_secret, tenant

AVAILABILITY_STATUS = {
    "0": "available",
    "1": "busy",
    "2": "slots available",
    "3": "out of office",
    "-1": "none",
}


def _client() -> GraphClient:
    return GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)


def _get_business(client: GraphClient, business_id: Optional[str]) -> BookingBusiness:
    """Return the requested business, or the first one if no id is given."""
    businesses = client.solutions.booking_businesses.get().execute_query()
    if not businesses:
        print(
            "No booking businesses found. Create one with the 'create' subcommand "
            "or at https://outlook.office.com/bookings."
        )
        sys.exit(1)
    if business_id:
        match = next((b for b in businesses if b.id == business_id), None)
        if match is None:
            print(f"No booking business with id: {business_id}")
            sys.exit(1)
        return match
    return businesses[0]


def cmd_list(client: GraphClient, args: argparse.Namespace) -> None:
    businesses = client.solutions.booking_businesses.get().execute_query()
    print(f"Booking businesses: {len(businesses)}")
    for b in businesses:
        address = b.address
        city = address.city if address else "?"
        print(f"  {b.id:40s} {b.display_name or '(unnamed)':30s} city={city}")


def cmd_show(client: GraphClient, args: argparse.Namespace) -> None:
    biz = _get_business(client, args.business_id)
    print(f"Inspecting: {biz.display_name} ({biz.id})")

    print("  Business hours:")
    for wh in biz.business_hours:
        print(f"    {wh.day}  {wh.timeSlots}")

    services = biz.services.get().execute_query()
    print(f"\n  Services ({len(services)}):")
    for s in services:
        display = s.properties.get("displayName", "?")
        duration = s.properties.get("duration", "?")
        price = s.properties.get("defaultPrice", "?")
        print(f"    {display:35s}  duration={duration}  price={price}")

    staff = biz.staff_members.get().execute_query()
    print(f"\n  Staff members ({len(staff)}):")
    for s in staff:
        name = s.properties.get("displayName", "?")
        email = s.properties.get("emailAddress", "?")
        print(f"    {name:25s}  {email}")

    customers = biz.customers.get().execute_query()
    print(f"\n  Customers: {len(customers)}")


def cmd_availability(client: GraphClient, args: argparse.Namespace) -> None:
    biz = _get_business(client, args.business_id)
    staff = biz.staff_members.get().execute_query()
    if not staff:
        print("No staff members found.")
        return

    now = datetime.now(timezone.utc)
    result = biz.get_staff_availability(
        staff_ids=[s.id for s in staff if s.id],
        start_datetime=now,
        end_datetime=now + timedelta(days=args.days),
    ).execute_query()

    for item in result.value:
        name = next((s.properties.get("displayName", "?") for s in staff if s.id == item.staffId), item.staffId)
        print(f"\n  {name}:")
        for slot in item.availabilityItems:
            status = AVAILABILITY_STATUS.get(str(slot.status.value), str(slot.status.value))
            start = slot.startDateTime
            end = slot.endDateTime
            print(f"    {status:15s} {start} -> {end}")


def cmd_add_appointment(client: GraphClient, args: argparse.Namespace) -> None:
    biz = _get_business(client, args.business_id)
    services = biz.services.get().execute_query()
    if not services:
        print("No services found.")
        return

    service = services[0]
    now = datetime.now(timezone.utc)
    start = now + timedelta(days=1, hours=9)
    end = start + timedelta(hours=1)

    appointment = biz.appointments.add(
        serviceId=service.id,
        serviceName=service.properties.get("displayName", "Consultation"),
        startDateTime=DateTimeTimeZone.parse(start),
        endDateTime=DateTimeTimeZone.parse(end),
        customerEmail=args.customer_email,
        customerName=args.customer_name,
        customerPhone=args.customer_phone,
        additionalInformation="Initial consultation booking via API",
    ).execute_query()
    print(f"✓ Appointment created: {appointment.id}")


def cmd_add_customer(client: GraphClient, args: argparse.Namespace) -> None:
    biz = _get_business(client, args.business_id)
    customer = biz.customers.add(displayName=args.name, emailAddress=args.email).execute_query()
    print(f"✓ Customer added: {customer.id}")


def cmd_create(client: GraphClient, args: argparse.Namespace) -> None:
    business = client.solutions.booking_businesses.add(args.name).execute_query()
    print(f"✓ Created business: {business.display_name} ({business.id})")


def cmd_publish(client: GraphClient, args: argparse.Namespace) -> None:
    biz = _get_business(client, args.business_id)
    biz.publish().execute_query()
    print(f"✓ Scheduling page published: {biz.properties.get('publicUrl', '?')}")


def _add_business_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--id", dest="business_id", default=None, help="booking business id (defaults to the first business)"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Microsoft Bookings businesses")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="list booking businesses")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="show business details")
    _add_business_arg(p)
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("availability", help="staff availability for the next N days")
    _add_business_arg(p)
    p.add_argument("--days", type=int, default=7, help="number of days to look ahead (default 7)")
    p.set_defaults(func=cmd_availability)

    p = sub.add_parser("add-appointment", help="book an appointment")
    _add_business_arg(p)
    p.add_argument("--customer-email", required=True, help="customer email address")
    p.add_argument("--customer-name", default="John Doe", help="customer display name")
    p.add_argument("--customer-phone", default="+1 555 123 4567", help="customer phone number")
    p.set_defaults(func=cmd_add_appointment)

    p = sub.add_parser("add-customer", help="add a customer")
    _add_business_arg(p)
    p.add_argument("--name", required=True, help="customer display name")
    p.add_argument("--email", required=True, help="customer email address")
    p.set_defaults(func=cmd_add_customer)

    p = sub.add_parser("create", help="create a booking business")
    p.add_argument("--name", default="SDK Demo Consulting", help="business display name")
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("publish", help="publish the scheduling page")
    _add_business_arg(p)
    p.set_defaults(func=cmd_publish)

    return parser


def main():
    args = build_parser().parse_args()
    args.func(_client(), args)


if __name__ == "__main__":
    main()
