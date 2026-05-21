from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class SelfSignedCertificate(ClientValue):
    """Contains the public part of a signing certificate.

    :param custom_key_identifier: 	Custom key identifier.
    :param str display_name: The friendly name for the key.
    :param end_datetime: The date and time at which the credential expires. The timestamp type represents date
         and time information using ISO 8601 format and is always in UTC time
    :param key: The value for the key credential. Should be a Base-64 encoded value.
    :param key_id: 	The unique identifier (GUID) for the key.
    :param start_datetime: The date and time at which the credential becomes valid. The timestamp type represents
         date and time information using ISO 8601 format and is always in UTC time
    :param thumbprint: 	The thumbprint value for the key.
    :param type_: 	The type of key credential. AsymmetricX509Cert.
    :param usage: A string that describes the purpose for which the key can be used. The possible value is Verify.
    """

    customKeyIdentifier: str | None = None
    displayName: str | None = None
    endDateTime: datetime | None = None
    key: str | None = None
    keyId: str | None = None
    startDateTime: datetime | None = None
    thumbprint: str | None = None
    type: str | None = None
    usage: str | None = None
