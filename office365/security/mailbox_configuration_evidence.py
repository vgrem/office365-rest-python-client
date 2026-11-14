from __future__ import annotations

from uuid import UUID

from office365.security.alerts.evidence import AlertEvidence
from office365.security.mailbox_configuration_type import (
    MailboxConfigurationType,
)


class MailboxConfigurationEvidence(AlertEvidence):
    configurationId: str | None = None
    displayName: str | None = None
    externalDirectoryObjectId: UUID | None = None
    mailboxPrimaryAddress: str | None = None
    upn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.MailboxConfigurationEvidence"

    configurationType: MailboxConfigurationType = MailboxConfigurationType.mailForwardingRule
