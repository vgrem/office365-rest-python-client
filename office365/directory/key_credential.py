from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class KeyCredential(ClientValue):
    """Contains a key credential associated with an application .
    The keyCredentials property of the application entity is a collection of keyCredential.

    :param str custom_key_identifier: A 40-character binary type that can be used to identify the credential.
       Optional. When not provided in the payload, defaults to the thumbprint of the certificate.
    :param str display_name: Friendly name for the key. Optional.
    :param datetime.datetime or str end_datetime: The date and time at which the credential expires.
        The DateTimeOffset type represents date and time information using ISO 8601 format and is always in UTC time
        For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z.
    :param bytes or str key: The certificate's raw data in byte array converted to Base64 string.
        Returned only on $select for a single object, that is,
        GET applications/{applicationId}?$select=keyCredentials or
        GET servicePrincipals/{servicePrincipalId}?$select=keyCredentials; otherwise, it is always null.
    :param str key_id: The unique identifier (GUID) for the key.
    :param datetime.datetime or start_datetime: The date and time at which the credential becomes valid.The Timestamp
        type represents date and time information using ISO 8601 format and is always in UTC time.
        For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z.
    :param str key_type: The type of key credential; for example, Symmetric, AsymmetricX509Cert.
    :param str usage: A string that describes the purpose for which the key can be used; for example, Verify.
    """

    customKeyIdentifier: str | None = None
    displayName: str | None = None
    endDateTime: datetime | str | None = None
    key: str | None = None
    keyId: str | None = None
    startDateTime: datetime | str | None = None
    type: str | None = None
    usage: str | None = None

    def __str__(self):
        return self.displayName or self.entity_type_name

    @property
    def entity_type_name(self):
        return "microsoft.graph.KeyCredential"
