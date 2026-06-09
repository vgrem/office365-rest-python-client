from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.subscriptions.encrypted_content import ChangeNotificationEncryptedContent
from office365.subscriptions.resource_data import ResourceData


@dataclass
class ChangeNotification(ClientValue):
    """Represents the notification sent to the subscriber.

    Args:
        change_type (str): Indicates the type of change that will raise the change notification. The supported values are: created, updated, deleted. Required.
        client_state (str): Value of the clientState property sent in the subscription request (if any). The maximum length is 255 characters. The client can check whether the change notification came from the service by comparing the values of the clientState property. The value of the clientState property sent with the subscription is compared with the value of the clientState property received with each change notification. Optional.
        encrypted_content (ChangeNotificationEncryptedContent): Encrypted content attached with the change notification. Only provided if encryptionCertificate and includeResourceData were defined during the subscription request and if the resource supports it. Optional.
        resource (str): The URI of the resource that emitted the change notification relative to https://graph.microsoft.com. Required
        resource_data (ResourceData): The content of this property depends on the type of resource being subscribed to. Optional.
    """

    changeType: str | None = None
    clientState: str | None = None
    encryptedContent: ChangeNotificationEncryptedContent = field(default_factory=ChangeNotificationEncryptedContent)
    resource: str | None = None
    resourceData: ResourceData = field(default_factory=ResourceData)
