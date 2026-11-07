# Exchange admin client

Run Exchange admin calls from Python and read the results as dictionaries —
mailboxes, mailbox folder permissions, and organisation configuration.

```python
from office365.admin.exchange import ExchangeAdminClient
```

## Install

```bash
pip install office365-rest-python-client
```

## What the tenant needs

* An app registration, with a secret or a certificate.
* **An admin has granted** `Exchange.ManageAsAppV2` (app-only) or `Exchange.ManageV2`
  (delegated).
* **An Exchange role assigned to that app** (or user). The permission alone is not
  enough: a call without a role is refused with `403`.
* Your tenant id — it goes into the address of every call.

## Sign in

**App-only, with a secret.** An app has no mailbox of its own, so every call carries a
routing key naming the mailbox it is about (`anchor`). For calls that are not about any
particular mailbox, use the system mailbox:

```python
import os

from office365.admin.exchange import ExchangeAdminClient

tenant_id = os.environ["O365_TENANT_ID"]

client = ExchangeAdminClient(
    tenant_id,
    anchor=ExchangeAdminClient.system_mailbox_anchor(tenant_id),
).with_client_secret(os.environ["O365_CLIENT_ID"], os.environ["O365_CLIENT_SECRET"])
```

**App-only, with a certificate:**

```python
client = ExchangeAdminClient(tenant_id, anchor=ExchangeAdminClient.system_mailbox_anchor(tenant_id)).with_certificate(
    client_id, thumbprint=thumbprint, private_key=private_key_path
)
```

**Delegated, as the signed-in admin** — the anchor is that admin's address:

```python
client = ExchangeAdminClient(tenant_id, anchor="AAD-UPN:admin@contoso.com").with_device_flow(client_id)
```

Also available: `with_token_interactive()` (browser window), `with_username_and_password()`
(test tenants only — it fails under MFA). If you already hold a token:

```python
client.pending_request().with_access_token(lambda: {"access_token": token, "token_type": "Bearer"})
```

### Choosing the mailbox (`anchor`)

| Value | Targets |
|---|---|
| `AAD-UPN:adele@contoso.com` | that user's mailbox |
| `AAD-SMTP:adele@contoso.com` | same, by SMTP address |
| `MBX:<mailbox-guid>@<tenant>` | same, by Exchange mailbox GUID |
| `APP:SystemMailbox{bb558c35-97f1-4cb9-8ff7-d53741dc928c}@<tenant>` | no particular mailbox |

Set it once on the client, or override it on a single call with `anchor=`.

## Use it

Every call is queued and then executed; the result is the service's JSON:

```python
config = client.get_organization_config().execute_query()
print(config.value["Name"])
```

Read a whole collection — paging is handled for you:

```python
for mailbox in client.get_mailboxes(select=["DisplayName", "PrimarySmtpAddress"]):
    print(mailbox["DisplayName"], mailbox["PrimarySmtpAddress"])
```

`select` asks for fewer properties, so the call comes back sooner; `result_size` sets
the page size (default 1000).

Mailbox folder permissions — the anchor comes from the identity you pass:

```python
identity = "adele@contoso.com:\\Calendar"

for entry in client.get_mailbox_folder_permissions(identity).execute_query().value:
    print(entry["User"]["DisplayName"], entry["AccessRights"])

client.add_mailbox_folder_permission(identity, user="alex@contoso.com", access_rights=["Reviewer"]).execute_query()
client.set_mailbox_folder_permission(identity, user="alex@contoso.com", access_rights=["Editor"]).execute_query()
client.remove_mailbox_folder_permission(identity, user="alex@contoso.com").execute_query()
```

Anything without a wrapper is one call away:

```python
result = client.invoke("Mailbox", "Get-Mailbox", {"ResultSize": 10}, select=["DisplayName"]).execute_query()

for mailbox in result.value:
    print(mailbox["DisplayName"])
```

`invoke_all(...)` is the same thing but follows every page for you, like `get_mailboxes()`.

## When a call fails

```python
from office365.runtime.client_request_exception import ClientRequestException

try:
    client.get_organization_config().execute_query()
except ClientRequestException as exc:
    print(exc)  # ('BadRequest', 'The parameter is not supported.')
```

| Status | Usual cause |
|---|---|
| `400` | the cmdlet, or one of its parameters, is not supported |
| `401` | the token is not for Exchange, or has expired |
| `403` | the token is fine — the app has no Exchange role for this operation |

Retries on throttling and transient errors, rate limiting, `await execute_query_async()`
and `execute_query_parallel(concurrency=4)` all come with the client.
Batching is not available — one call is one request.

## Coverage

The published surface is deliberately small: `Mailbox`, `MailboxFolderPermission`,
`OrganizationConfig`, `AcceptedDomain`, `DistributionGroupMember` and
`DynamicDistributionGroupMember`. If a call you need is not on that list, it is not
available through this client.

## Clouds

| Environment | Host |
|---|---|
| `Global` and `USGovernment` | `https://outlook.office365.com` |
| `USGovernmentHigh` | `https://outlook.office365.us` |
| `USGovernmentDoD` | `https://outlook-dod.office365.us` |
| `China` | `https://outlook.office365.cn` |

```python
from office365.azure_env import AzureEnvironment

client = ExchangeAdminClient(tenant_id, environment=AzureEnvironment.USGovernmentHigh)
```
