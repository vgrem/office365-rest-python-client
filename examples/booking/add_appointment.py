"""
Book an appointment with a customer for the first service of a business.

Requires delegated permission ``BookingsAppointment.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/bookingbusiness-post-appointments
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Book a booking appointment")
    parser.add_argument("--id", required=True, help="booking business id")
    parser.add_argument("--customer-email", required=True, help="customer email address")
    parser.add_argument("--customer-name", default="John Doe", help="customer display name")
    parser.add_argument("--customer-phone", default="+1 555 123 4567", help="customer phone number")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    businesses = client.solutions.booking_businesses.get().execute_query()
    biz = next((b for b in businesses if b.id == args.id), None)
    if biz is None:
        sys.exit(f"No booking business with id: {args.id}")

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


if __name__ == "__main__":
    main()
