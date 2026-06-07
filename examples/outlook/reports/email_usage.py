"""
Usage report: email activity and mailbox usage across periods.

Compares D7, D30, and D90 activity counts plus mailbox storage
usage — useful for adoption tracking, cleanup planning, and
audit reporting.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getemailactivitycounts
https://learn.microsoft.com/en-us/graph/api/reportroot-getmailboxusagestorage
https://learn.microsoft.com/en-us/graph/api/reportroot-getmailboxusagemailboxcounts
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

PERIODS = ["D7", "D30", "D90"]

print("Email activity report\n")

for p in PERIODS:
    counts = client.reports.get_email_activity_counts(p).execute_query()
    print(f"  Activity counts ({p}): {counts.value}")

print()

storage = client.reports.get_mailbox_usage_storage("D90").execute_query()
print(f"  Mailbox storage (D90): {storage.value}")

mailbox_counts = client.reports.get_mailbox_usage_mailbox_counts("D90").execute_query()
print(f"  Mailbox counts (D90): {mailbox_counts.value}")
