from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.mailbox_configuration_type import (
    MailboxConfigurationType,
)


@value
class MailboxConfigurationEvidence(ClientValue):
    configurationId: str | None = None
    displayName: str | None = None
    externalDirectoryObjectId: UUID | None = None
    mailboxPrimaryAddress: str | None = None
    upn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.MailboxConfigurationEvidence"

    configurationType: MailboxConfigurationType = MailboxConfigurationType.mailForwardingRule
