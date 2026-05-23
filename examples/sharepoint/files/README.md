## Getting started

All examples use the same pattern:

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Pick an example and pass `ctx`:
file = ctx.web.get_file_by_server_relative_url("/sites/team/Shared Documents/report.docx")
file.download("report.docx").execute_query()
```
