from typing import Dict, List

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class EmailProperties(ClientValue):

    def __init__(
        self,
        body: str,
        subject: str,
        to: List[str],
        from_address: str = None,
        cc: List[str] = None,
        bcc: List[str] = None,
        additional_headers: Dict = None,
        from_: str = None,
    ):
        """
        Specifies the definition of the email to send which includes both the message fields and body

        :param str body: Specifies the message body to send.
        :param str subject: Specifies the Subject field of the e-mail.
        :param list[str] to: Specifies the To field of the email.
        :param str or None from_address: Specifies the From field of the email.
        :param list[str] or None cc: Specifies the carbon copy (cc) recipients of the email.
        :param list[str] or None bcc: Specifies the blind carbon copy (bcc) recipients of the email
        :param dict or None additional_headers:
        """
        super().__init__()
        self.Body = body
        self.Subject = subject
        self.From = from_address
        self.To = StringCollection(to)
        self.CC = StringCollection(cc)
        self.BCC = StringCollection(bcc)
        self.AdditionalHeaders = additional_headers
        self.From = from_

    @property
    def entity_type_name(self):
        return "SP.Utilities.EmailProperties"
