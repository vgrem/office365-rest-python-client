# Webs

A **web** (also called a site) is a SharePoint container for lists, libraries,
and pages. Every site has one root web and optionally many subsites.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Read access** to the web | Required to read properties and lists. **Site Owner** for configuration operations. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## How webs are structured

```mermaid
graph TD
    Root["Root Web\n(/sites/team)"]
    Sub1["Subsite\n(/sites/team/hr)"]
    Sub2["Subsite\n(/sites/team/it)"]
    List["Lists /\nLibraries"]
    SubSub["Sub-subsite\n(/sites/team/hr/benefits)"]

    Root --> Sub1
    Root --> Sub2
    Root --> List
    Sub1 --> SubSub
```

Every site has a root web. Webs can nest as subsites to form a hierarchy.
The current context's `web` property represents the site you're connected to.

---

## Examples

### Read

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | Get web properties | [`get_props.py`](./get_props.py) | Read access | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **2** | Subsite inventory (template, created, language) | [`get_all.py`](./get_all.py) | Read access | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **3** | Lists inventory (items, template, created) | [`get_lists.py`](./get_lists.py) | Read access | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **4** | Permissions matrix (roles + who has access) | [`get_roles.py`](./get_roles.py) | Read access | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **5** | Regional settings + timezone conversion | [`get_regional_settings.py`](./get_regional_settings.py) | Read access | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **6** | Recent changes report (grouped by type) | [`get_changes.py`](./get_changes.py) | Read access | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **7** | Site metadata summary (version, URLs) | [`print_version.py`](./print_version.py) | Read access | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **8** | Get activities | [`get_activities.py`](./get_activities.py) | Read access | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **9** | Get web from absolute URL | [`get_from_abs_url.py`](./get_from_abs_url.py) | Read access on target | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

### Configure

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **10** | Enable Document ID | [`enable_doc_id.py`](./enable_doc_id.py) | Site Owner | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **11** | Clear a web (remove all content, `--dry-run` supported) | [`clear_web.py`](./clear_web.py) | Site Owner | [Webs REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# Get web properties
web = ctx.web.get().execute_query()
print(f"Title: {web.title}, URL: {web.url}, Template: {web.get_web_template()}")
```

---

## API reference

- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
