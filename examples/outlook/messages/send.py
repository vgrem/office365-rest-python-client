"""
Send a message with a recipient, subject, and body.

The simplest way to send email via the Graph API.

Requires delegated permission ``Mail.Send``.

https://learn.microsoft.com/en-us/graph/api/user-sendmail
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, user_principal, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

client.me.send_mail(
    subject="Hello from Graph API",
    body="This email was sent using the Microsoft Graph API.",
    to_recipients=[user_principal],
).execute_query()
print("Message sent")
