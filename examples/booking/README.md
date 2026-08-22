# Microsoft Bookings

Examples for managing Bookings businesses, services, appointments, staff, and customers.

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Bookings.ReadWrite.All` | Read and manage booking businesses, services, staff | [Bookings permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#bookings-permissions) |
| `BookingsAppointment.ReadWrite.All` | Create and manage appointments | [Bookings permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#bookings-permissions) |

## Examples

Run from the repo root. Auth is app-only via the credentials in `tests/settings.py`; every
business-targeted script takes `--id` (find ids with `list_businesses.py`).

| Operation | File | Permission |
|---|---|---|
| List booking businesses | [`list_businesses.py`](./list_businesses.py) | `Bookings.Read.All` |
| Show business details (hours, services, staff, customers) | [`show_business.py`](./show_business.py) | `Bookings.Read.All` |
| Staff availability for the next N days | [`staff_availability.py`](./staff_availability.py) | `Bookings.Read.All` |
| Book an appointment | [`add_appointment.py`](./add_appointment.py) | `BookingsAppointment.ReadWrite.All` |
| Add a customer | [`add_customer.py`](./add_customer.py) | `Bookings.ReadWrite.All` |
| Create a booking business | [`create_business.py`](./create_business.py) | `Bookings.ReadWrite.All` |
| Publish the scheduling page | [`publish_business.py`](./publish_business.py) | `Bookings.ReadWrite.All` |

### Quick start

```bash
python examples/booking/list_businesses.py
python examples/booking/show_business.py --id <business_id>
python examples/booking/staff_availability.py --id <business_id> [--days 7]
python examples/booking/add_appointment.py --id <business_id> --customer-email client@example.com
python examples/booking/add_customer.py --id <business_id> --name "Jane Doe" --email jane@example.com
python examples/booking/create_business.py [--name "Demo Consulting"]
python examples/booking/publish_business.py --id <business_id>
```
