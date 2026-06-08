# SharePoint REST API Examples

This directory contains examples for the SharePoint REST API v1
(`office365.sharepoint`). Each example uses a minimal auth setup and
prints clear output.

---

## Directories

| Directory | Covers |
|---|---|
| [`app-catalog/`](./app-catalog/) | SPFx app lifecycle |
| [`alerts/`](./alerts/) | Email notifications on list/item changes |
| [`audit/`](./audit/) | Audit settings, sign-in logs |
| [`auth/`](./auth/) | Modern MSAL auth, legacy ACS/SAML, on-prem NTLM, cookie capture |
| [`contenttypes/`](./contenttypes/) | Content types, field links, hierarchy |
| [`customactions/`](./customactions/) | Custom action bindings (legacy) |
| [`eventreceivers/`](./eventreceivers/) | Remote event receivers (legacy) |
| [`features/`](./features/) | Site features activation |
| [`fields/`](./fields/) | Site/list column CRUD (all types) |
| [`files/`](./files/) | Upload, download, copy, move, check out, versions, permissions |
| [`folders/`](./folders/) | Create, copy, move, rename, delete folders |
| [`groups/`](./groups/) | SharePoint groups management |
| [`hubsites/`](./hubsites/) | Hub site registration, association |
| [`listitems/`](./listitems/) | Item CRUD, bulk operations, filters, attachments |
| [`lists/`](./lists/) | List CRUD, import/export, paging |
| [`migration/`](./migration/) | Migration assessment scanner |
| [`navigation/`](./navigation/) | Top nav, Quick Launch |
| [`pages/`](./pages/) | Modern site pages CRUD, news |
| [`propertybag/`](./propertybag/) | Custom key-value pairs on webs |
| [`permissions/`](./permissions/) | Grant, revoke, break inheritance |
| [`recyclebin/`](./recyclebin/) | Restore deleted items |
| [`search/`](./search/) | KQL queries, filters, refinement |
| [`sharing/`](./sharing/) | Sharing links, anonymous access |
| [`sitedesigns/`](./sitedesigns/) | Site designs and site scripts |
| [`sites/`](./sites/) | Create (modern/classic/communication), manage admins |
| [`sitescripts/`](./sitescripts/) | Site script JSON actions |
| [`taxonomy/`](./taxonomy/) | Term store, term sets, managed metadata |
| [`teams/`](./teams/) | Teams via SharePoint API (limited) |
| [`tenant/`](./tenant/) | Tenant admin, site collections, licensing |
| [`userprofile/`](./userprofile/) | Profile properties, followers, OneDrive URL |
| [`users/`](./users/) | Current user, site users, search |
| [`views/`](./views/) | List views, default and custom |
| [`webhooks/`](./webhooks/) | List/webhook subscriptions |
| [`advanced/`](./advanced/) | Proxy config, SSL, performance diagnostics, raw requests |
| [`webs/`](./webs/) | Web properties, subsites, changes, regional settings |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

web = ctx.web.get().execute_query()
print(f"Connected to: {web.title}  ({web.url})")
```

---

## API reference

- [SharePoint REST API overview](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
