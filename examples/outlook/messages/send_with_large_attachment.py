"""
Send a message with a large file attachment via upload session.

Files larger than ~3 MB require an upload session instead of
inline attachment.

Requires delegated permission ``Mail.ReadWrite`` and ``Mail.Send``.

https://learn.microsoft.com/en-us/graph/api/attachment-createuploadsession
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, user_principal, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

local_path = "../../../tests/data/big_buck_bunny.mp4"


def print_progress(range_pos: int) -> None:
    print(f"{range_pos} bytes uploaded")


message = (
    (
        client.me.messages.add(
            subject="Meet for lunch?",
            body="The new cafeteria is open.",
            to_recipients=[
                "fannyd@contoso.onmicrosoft.com",
                "vvgrem@gmail.com",
                user_principal,
            ],
        ).upload_attachment(local_path, print_progress)
    )
    .send()
    .execute_query()
)
print("Message sent with attachment")
