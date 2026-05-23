# SharePoint Webhook Subscriptions

Webhooks let your app receive HTTP callbacks when items change in a SharePoint list.
Subscriptions are scoped to a single list and expire after 180 days (renew by updating `expiration_datetime`).

| What | File | Notes |
|------|------|-------|
| **Add subscription** | [`add_subscription.py`](./add_subscription.py) | Subscribe to list change notifications |
| **List subscriptions** | [`get_subscriptions.py`](./get_subscriptions.py) | Enumerate subscriptions on a list |
| **Update expiration** | [`set_expiration.py`](./set_expiration.py) | Extend or renew a subscription |
| **Remove subscription** | [`remove_subscription.py`](./remove_subscription.py) | Unsubscribe from notifications |

---

## Official docs

- [SharePoint webhooks overview](https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-webhooks)
- [SharePoint list webhooks reference](https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-list-webhooks)
