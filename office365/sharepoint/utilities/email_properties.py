

from __future__ import annotations
from typing import Dict, List, Optional

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class EmailProperties(ClientValue):

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

    Body: str
    Subject: str
    From: Optional[str] = None
    To: StringCollection
    CC: StringCollection | None = None
    BCC: StringCollection | None = None
    AdditionalHeaders: Optional[Dict] = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.EmailProperties"
