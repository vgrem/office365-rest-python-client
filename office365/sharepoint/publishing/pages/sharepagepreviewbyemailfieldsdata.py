from typing import List, Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SharePagePreviewByEmailFieldsData(ClientValue):
    """This class contains the information used by SharePagePreviewByEmail method"""

    def __init__(self, message: Optional[str] = None, recipient_emails: Optional[List[str]] = None):
        """
        :param str message:
        :param list[str] recipient_emails:
        """
        self.message = message
        self.recipientEmails = StringCollection(recipient_emails)

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePagePreviewByEmailFieldsData"
