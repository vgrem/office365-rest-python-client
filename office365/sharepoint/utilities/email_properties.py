from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class EmailProperties(ClientValue):
    """Specifies the definition of the email to send which includes both the message fields and body

    Args:
        body (str): Specifies the message body to send.
        subject (str): Specifies the Subject field of the e-mail.
        to (list[str]): Specifies the To field of the email.
        from_address (str or None): Specifies the From field of the email.
        cc (list[str] or None): Specifies the carbon copy (cc) recipients of the email.
        bcc (list[str] or None): Specifies the blind carbon copy (bcc) recipients of the email
        additional_headers (dict or None):
    """

    Body: str
    Subject: str
    To: StringCollection
    From: Optional[str] = None
    CC: StringCollection | None = None
    BCC: StringCollection | None = None
    AdditionalHeaders: Optional[Dict] = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.EmailProperties"
