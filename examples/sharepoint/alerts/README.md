# SharePoint Alerts

Examples for managing SharePoint alerts — list, create, and remove
alerts on lists and document libraries.

Alerts are associated with the **current user**, not with the list
directly. To create an alert on a list, you add it to the user's
alert collection with the list URL as the target.

---

## Prerequisites

| Permission | Description |
|---|---|
| `Sites.Read.All` | List alerts |
| `Sites.ReadWrite.All` | Create and remove alerts |

---

## Examples

| Scenario | File |
|---|---|
| List alerts for the current user | [`list_alerts.py`](./list_alerts.py) |
| Add an alert on a list | [`add_alert.py`](./add_alert.py) |
| Remove an alert by ID | [`remove_alert.py`](./remove_alert.py) |

---

## Official docs

- [SharePoint alerts REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
