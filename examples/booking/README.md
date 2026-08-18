# Microsoft Bookings

Examples for managing Bookings businesses, services, appointments, staff, and customers.

## [`manage.py`](./manage.py) — CLI

Run from the repo root. Requires the credentials in `tests/settings.py` (client id, secret, tenant).

```bash
python examples/booking/manage.py list                          # list booking businesses
python examples/booking/manage.py show [--id <business_id>]     # business hours, services, staff, customers
python examples/booking/manage.py availability [--id] [--days 7]  # staff availability for the next N days
python examples/booking/manage.py add-appointment --customer-email client@example.com [--id]
python examples/booking/manage.py add-customer --name "Jane Doe" --email jane@example.com [--id]
python examples/booking/manage.py create [--name "Demo Consulting"]
python examples/booking/manage.py publish [--id]
```

Every subcommand that targets a business defaults to the first one; pass `--id` to select another.

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Bookings.ReadWrite.All` | Read and manage booking businesses, services, staff | [Bookings permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#bookings-permissions) |
| `BookingsAppointment.ReadWrite.All` | Create and manage appointments | [Bookings permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#bookings-permissions) |
