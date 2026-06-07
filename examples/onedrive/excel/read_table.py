"""
Read Excel tables and range data using workbook sessions.

Workbook sessions allow consistent reads across a workbook.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/resources/excel
https://learn.microsoft.com/en-us/graph/api/workbook-list-tables
https://learn.microsoft.com/en-us/graph/api/workbook-tablerow-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

# Find an Excel file
items = client.me.drive.search("*.xlsx").execute_query()
if len(items) == 0:
    exit("No Excel files found. Upload one first.")

workbook = items[0].workbook

# 1. Start a workbook session
try:
    session = workbook.create_session(persist_changes=False).execute_query()
    print(f"Session created: {session.id}")
except Exception:
    pass  # Sessions may not be required for all operations

# 2. List tables
tables = workbook.tables.get().execute_query()
print(f"Tables ({len(tables)}):")
for t in tables:
    rows = t.rows.get().execute_query()
    print(f"  {t.name:30s}  rows: {len(rows)}")
