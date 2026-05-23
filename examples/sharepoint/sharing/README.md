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
| **Share a file (org-wide)** | [`share_file_organizational.py`](./share_file_organizational.py) | Company-wide link |
| **Share a file with password** | [`share_file_with_password.py`](./share_file_with_password.py) | Password-protected link |
| **Share a folder** | [`share_folder.py`](./share_folder.py) | With specific people |
| **Share a folder (org-wide)** | [`share_folder_organizational.py`](./share_folder_organizational.py) | Company-wide link |
| **Share a folder (anonymous)** | [`share_folder_anonymous.py`](./share_folder_anonymous.py) | Anonymous "Anyone" link |
| **Share a web / site** | [`share_web.py`](./share_web.py) | Grant access to a site |
| **Create anonymous link** | [`create_anonymous_link.py`](./create_anonymous_link.py) | "Anyone with the link" |
| **Update sharing link** | [`update_sharing_link.py`](./update_sharing_link.py) | Change expiration date |
| **Remove sharing link** | [`remove_sharing_link.py`](./remove_sharing_link.py) | Delete an existing link |
| **Get file sharing info** | [`get_file_sharing_info.py`](./get_file_sharing_info.py) | Links, users, permissions |
| **Get folder sharing info** | [`get_folder_sharing_info.py`](./get_folder_sharing_info.py) | Links, permissions, audience |
| **Get site sharing** | [`get_site_sharing.py`](./get_site_sharing.py) | Current sharing capability |
| **Set site sharing** | [`set_site_sharing.py`](./set_site_sharing.py) | Change sharing capability |

---

## Official docs

- [SharePoint sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api)
