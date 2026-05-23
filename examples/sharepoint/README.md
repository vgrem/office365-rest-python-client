# SharePoint REST API Examples

This directory contains examples for the SharePoint REST API v1
(`office365.sharepoint`). Each example uses a minimal auth setup and
prints clear output.

---

## 📁 Category guides

| Directory | README | Covers |
|-----------|--------|--------|
| [`alm/`](./alm/) | [README](./alm/README.md) | SPFx app lifecycle — upload, deploy, install, uninstall |
| [`files/`](./files/) | [README](./files/README.md) | Upload, download, copy, move, share, versions, permissions |
| [`listitems/`](./listitems/) | [README](./listitems/README.md) | CRUD, bulk operations, attachments, filters, field values |
| [`lists/`](./lists/) | [README](./lists/README.md) | Create, read, import, export, filter, paging |
| [`folders/`](./folders/) | [README](./folders/README.md) | Create, delete, copy, move, share, list |
| [`sites/`](./sites/) | [README](./sites/README.md) | Create, delete, clone, status |
| [`webs/`](./webs/) | [README](./webs/README.md) | Properties, lists, roles, changes, activities |
| [`tenant/`](./tenant/) | [README](./tenant/README.md) | Site collections, admin, licensing |
| [`fields/`](./fields/) | [README](./fields/README.md) | Create lookup, date, choice, taxonomy fields |
| [`sharing/`](./sharing/) | [README](./sharing/README.md) | Share files/folders, create anonymous links |
| [`search/`](./search/) | [README](./search/README.md) | Query sites, content, sorting |
| [`taxonomy/`](./taxonomy/) | [README](./taxonomy/README.md) | Term sets, term groups, managed metadata |
| [`users/`](./users/) | *(coming soon)* | Current user, site users, permissions |
| [`permissions/`](./permissions/) | *(coming soon)* | Grant, revoke, check permissions |
| [`pages/`](./pages/) | *(coming soon)* | Create and publish pages |
| [`views/`](./views/) | *(coming soon)* | Create and manage list views |
| [`contenttypes/`](./contenttypes/) | *(coming soon)* | Create and manage content types |
| [`features/`](./features/) | *(coming soon)* | Activate and deactivate site features |
| [`auth/`](./auth/) | [README](./auth/README.md) | Modern MSAL auth + legacy (SAML, NTLM) |

### Smaller categories

[`apps/`](./apps/) · [`audit/`](./audit/) · [`groups/`](./groups/) ·
[`hubsites/`](./hubsites/) · [`migration/`](./migration/) · [`navigation/`](./navigation/) ·
[`pushnotifications/`](./pushnotifications/) · [`sitedesigns/`](./sitedesigns/) ·
[`sitescripts/`](./sitescripts/) · [`teams/`](./teams/) · [`userprofile/`](./userprofile/)

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
