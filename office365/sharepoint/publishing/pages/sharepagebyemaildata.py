from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SharePageByEmailData(ClientValue):
    def __init__(
        self,
        bcc_emails: StringCollection = StringCollection(),
        cc_emails: StringCollection = StringCollection(),
        email_size: Optional[str] = None,
        message: Optional[str] = None,
        page_content: Optional[str] = None,
        page_item_id: Optional[int] = None,
        recipient_emails: StringCollection = StringCollection(),
        scenario_tag: Optional[str] = None,
        subject: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.BccEmails = bcc_emails
        self.CcEmails = cc_emails
        self.EmailSize = email_size
        self.Message = message
        self.PageContent = page_content
        self.PageItemId = page_item_id
        self.RecipientEmails = recipient_emails
        self.ScenarioTag = scenario_tag
        self.Subject = subject
        self.Url = url

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePageByEmailData"
