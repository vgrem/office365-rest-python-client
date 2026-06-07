"""
Send a message with a recipient, subject, and body.

The simplest way to send email via the Graph API.

Requires delegated permission ``Mail.Send``.

https://learn.microsoft.com/en-us/graph/api/user-sendmail
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_user_principal_name, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

client.me.send_mail(
    subject="Hello from Graph API",
    body="This email was sent using the Microsoft Graph API.",
    to_recipients=[test_user_principal_name],
).execute_query()
print("Message sent")
