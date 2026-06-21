"""
Send a message with a large file attachment via upload session.

Files larger than ~3 MB require an upload session instead of
inline attachment.

Requires delegated permission ``Mail.ReadWrite`` and ``Mail.Send``.

https://learn.microsoft.com/en-us/graph/api/attachment-createuploadsession
"""

from office365.graph_client import GraphClient
from office365.outlook.mail.attachments.attachment_item import AttachmentItem
from office365.outlook.mail.attachments.type import AttachmentType
from tests.settings import client_id, password, tenant, user_principal, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

draft = (
    client.me.messages.add(
        subject="Report with large attachment",
        body="Please find the report attached.",
        to_recipients=[user_principal],
    )
    .add_file_attachment("hello.txt", "Hello World!")
    .execute_query()
)

# Upload session for large attachments
attachment = AttachmentItem(
    attachmentType=AttachmentType.file,
    name="large_report.pdf",
    size=3483322,
)
session = draft.attachments.create_upload_session(attachment).execute_query()
print(f"Upload session created: {session.value}")

draft.send().execute_query()
print("Message sent with attachment")
