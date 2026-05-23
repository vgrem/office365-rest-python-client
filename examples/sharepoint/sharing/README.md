# Sharing in SharePoint

SharePoint supports several sharing models — anonymous links, company-wide
links, specific people, and external (guest) users. Every sharing operation
creates a **sharing link** that encodes the access level and audience.

This page groups examples by **what you want to do** — not by API endpoint.

---

## 🔗 Create Sharing Links

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Share a file with specific people (sends email)
ctx.web.get_file_by_server_relative_url("/sites/team/Shared Docs/report.docx")\
   .share("user@contoso.com", read_only=True).execute_query()

# Create an anonymous "Anyone" link
link = ctx.web.get_file_by_server_relative_url("/sites/team/Shared Docs/report.docx")\
   .create_anonymous_link().execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Share a file** | [`share_file.py`](./share_file.py) | With specific people |
| **Share a file (org-wide)** | [`share_file_org.py`](./share_file_org.py) | Company-wide link |
| **Share a file with password** | [`share_file_with_password.py`](./share_file_with_password.py) | Password-protected link |
| **Share a folder** | [`share_folder.py`](./share_folder.py) | With specific people |
| **Share a web / site** | [`share_web.py`](./share_web.py) | Grant access to a site |
| **Create anonymous link** | [`create_anon_link.py`](./create_anon_link.py) | "Anyone with the link" |

## 🔍 Get Sharing Info

| What | File | Notes |
|------|------|-------|
| **Get sharing info for a folder** | [`get_folder_sharing_info.py`](./get_folder_sharing_info.py) | Links, permissions, audience |

---

## Official docs

- [SharePoint sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api)
