from typing import List

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class RichSharing(Entity):
    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = ResourcePath("SP.Publishing.RichSharing")
        super().__init__(context, resource_path)

    def share_page_by_email(self, url: str, message: str, recipient_emails: List[str], page_content: str, subject: str):
        """Args:
        url (str):
        message (str):
        recipient_emails (list[str]):
        page_content (str):
        subject (str):
        """
        payload = {
            "url": url,
            "message": message,
            "recipientEmails": StringCollection(recipient_emails),
            "pageContent": page_content,
            "subject": subject,
        }
        qry = ServiceOperationQuery(self, "SharePageByEmail", None, payload)
        self.context.add_query(qry)
        return self

    def share_site_by_email(self, custom_description, custom_title, message, url, recipient_emails):
        """Args:
        url (str):
        message (str):
        recipient_emails (list[str]):
        custom_description (str):
        custom_title (str):
        """
        payload = {
            "Url": url,
            "Message": message,
            "recipientEmails": StringCollection(recipient_emails),
            "CustomTitle": custom_title,
            "CustomDescription": custom_description,
        }
        qry = ServiceOperationQuery(self, "ShareSiteByEmail", None, payload)
        self.context.add_query(qry)
        return self

    @property
    def entity_type_name(self):
        return "SP.Publishing.RichSharing"
