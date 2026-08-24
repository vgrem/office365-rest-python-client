# API Reference

A practical tour of what the library gives you: the two clients, authentication,
the query patterns that make it ergonomic, and the power-user features
(proxy, custom SSL, timeouts, concurrent batching, CSV export, throttling).

## The two clients

| | `ClientContext` | `GraphClient` |
|---|---|---|
| **Target API** | SharePoint REST API v1 | Microsoft Graph API |
| **Use for** | SharePoint lists, files, folders, search, site admin, permissions | Outlook, OneDrive, Teams, OneNote, Planner, Users, Groups |

```python
from office365.graph_client import GraphClient
from office365.sharepoint.client_context import ClientContext

graph = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret("client_id", "client_secret")

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)
```

## Authentication

Every modern flow is built in — client secret, certificate, username/password,
device code, and interactive (plus on-prem NTLM and cookies for SharePoint):

| Flow | `GraphClient` | `ClientContext` |
|---|---|---|
| Client secret | `with_client_secret(client_id, secret)` | `with_client_secret(tenant, client_id, secret)` |
| Certificate | `with_certificate(client_id, thumbprint, key)` | `with_client_certificate(tenant, client_id, thumbprint, cert_path)` |
| Username / password | `with_username_and_password(client_id, user, password)` | `with_username_and_password(tenant, client_id, user, password)` |
| Device code | `with_device_flow(client_id)` | `with_device_flow(tenant, client_id, scopes)` |
| Interactive | `with_token_interactive(client_id)` | `with_interactive(tenant, client_id, scopes)` |
| On-prem (NTLM) | — | `with_user_credentials(username, password)` |
| Cookies / custom | `with_token_callback(...)` | `with_cookies(...)`, `with_access_token(...)` |

See [the auth examples](auth/index.md) for full, runnable flows.

## Query patterns

### Filtering

OData `$filter` works identically on both clients:

```python
guests = client.users.filter("userType eq 'Guest'").get().execute_query()
files = ctx.web.lists.get_by_title("Documents").items.filter("FSObjType eq 0").get().execute_query()
```

For complex SharePoint queries, use a CAML query instead:

```python
from office365.sharepoint.listitems.caml.query import CamlQuery

qry = CamlQuery()
qry.ViewXml = "<View><Query><Where><Eq><FieldRef Name='Status'/><Value Type='Text'>Active</Value></Eq></Where></Query></View>"
items = ctx.web.lists.get_by_title("Tasks").get_items(qry).execute_query()
```

### Paging

`get_all()` follows server-driven paging (`@odata.nextLink`) so you never write
paging code:

```python
for user in client.users.get_all().execute_query():
    print(user.user_principal_name)
```

SharePoint collections expose `paged(page_size, page_loaded)` and
`get_all(page_size, page_loaded)`:

```python
all_items = ctx.web.lists.get_by_title("Contacts_Large").items.get_all(500).execute_query()
```

### Batching

Queue operations and submit them as a single OData `$batch` request — and run
several batches concurrently to cut wall time on large imports:

```python
target_list = ctx.web.lists.get_by_title("Documents")
for i in range(100):
    target_list.add_item({"Title": f"Item {i}"})
ctx.execute_batch(items_per_batch=100)      # one $batch request
ctx.execute_batch(concurrency=5)            # 5 batches in flight, retries on 429
```

### Throttling & retries

`execute_query_retry()` retries when Microsoft 365 throttles your request:

```python
result = client.users.top(10).get().execute_query_retry()
```

## Power features

### Proxy, custom SSL, timeouts

Configure the transport once — every request (including internal ones like the
form digest) inherits it:

```python
ctx = (
    ClientContext("https://contoso.sharepoint.com/sites/team")
    .with_client_certificate("tenant", "client_id", "thumbprint")
    .with_transport(
        proxies={"https": "http://proxy:8080"},
        verify="/path/to/ca-bundle.pem",   # or False for testing only
        timeout=30,
    )
)
```

> For MSAL authentication traffic to `login.microsoftonline.com`, set the
> `HTTPS_PROXY` environment variable instead — MSAL reads it directly.

### CSV export

Collections export straight to CSV (or a pandas DataFrame with the `pandas`
extra):

```python
with open("users.csv", "w", newline="") as f:
    client.users.get_all().select(["displayName", "userPrincipalName"]).to_csv(f).execute_query()
```

## Learn more

-   **[Products](products/index.md)** — start with the SharePoint area, then
    browse the rest from the left navigation.
-   **[Auth examples](auth/index.md)** — all authentication flows.
-   **[README](https://github.com/vgrem/office365-rest-python-client#readme)** —
    installation, the full auth matrix, and per-service guides.
