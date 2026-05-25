# SharePoint REST API Examples

This directory contains examples for the SharePoint REST API v1
(`office365.sharepoint`). Each example uses a minimal auth setup and
prints clear output.

---

## 📁 Category guides

| Directory | README | Covers |
|-----------|--------|--------|
| [`app-catalog/`](./app-catalog/) | [README](./app-catalog/README.md) | SPFx app lifecycle — upload, deploy, install, uninstall |
| [`files/`](./files/) | [README](./files/README.md) | Upload, download, copy, move, check out/in, publish, approve, share, versions, permissions |
| [`listitems/`](./listitems/) | [README](./listitems/README.md) | CRUD, bulk operations, attachments, filters, field values |
| [`lists/`](./lists/) | [README](./lists/README.md) | Create, read, import, export, filter, paging |
| [`folders/`](./folders/) | [README](./folders/README.md) | Create, delete, copy, move, share, list |
| [`sites/`](./sites/) | [README](./sites/README.md) | Create, delete, clone, status |
| [`webs/`](./webs/) | [README](./webs/README.md) | Properties, lists, roles, changes, activities |
| [`tenant/`](./tenant/) | [README](./tenant/README.md) | Site collections, admin, licensing |
| [`fields/`](./fields/) | [README](./fields/README.md) | CRUD for all field types — text, number, date, choice, lookup, user, taxonomy, calculated |
| [`sharing/`](./sharing/) | [README](./sharing/README.md) | Share files/folders, create anonymous links |
| [`search/`](./search/) | [README](./search/README.md) | Query sites, content, sorting |
| [`sitedesigns/`](./sitedesigns/) | [README](./sitedesigns/README.md) | Site designs, site scripts, provisioning automation |
| [`taxonomy/`](./taxonomy/) | [README](./taxonomy/README.md) | Term sets, term groups, managed metadata |
| [`users/`](./users/) | [README](./users/README.md) | Current user, site users, permissions |
| [`permissions/`](./permissions/) | [README](./permissions/README.md) | Grant, revoke, check, break/reset inheritance, role definitions |
| [`pages/`](./pages/) | [README](./pages/README.md) | Create and publish pages |
| [`views/`](./views/) | [README](./views/README.md) | Create and manage list views |
| [`contenttypes/`](./contenttypes/) | [README](./contenttypes/README.md) | Create and manage content types |
| [`features/`](./features/) | [README](./features/README.md) | Activate and deactivate site features |
| [`userprofile/`](./userprofile/) | [README](./userprofile/README.md) | Profile properties, followers, trending tags, OneDrive |
| [`navigation/`](./navigation/) | [README](./navigation/README.md) | Top nav, Quick Launch, add, update, delete nodes |
| [`hubsites/`](./hubsites/) | [README](./hubsites/README.md) | Hub sites — register, associate, home site |
| [`auth/`](./auth/) | [README](./auth/README.md) | Modern MSAL auth + legacy (SAML, NTLM) |

### Smaller categories

[`customactions/`](./customactions/) · [`eventreceivers/`](./eventreceivers/) ·
[`audit/`](./audit/) · [`groups/`](./groups/) ·
[`migration/`](./migration/) ·
[`webhooks/`](./webhooks/) · [`teams/`](./teams/)

---

## Getting started

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)
```

## Official docs

- [SharePoint REST API overview](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
