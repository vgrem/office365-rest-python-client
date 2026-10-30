from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.protection.policy.base import ProtectionPolicyBase
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.mailbox_protection_rule import MailboxProtectionRule
    from office365.common.mailbox_protection_unit import MailboxProtectionUnit
    from office365.common.mailbox_protection_units_bulk_addition_job import (
        MailboxProtectionUnitsBulkAdditionJob,
    )


class ExchangeProtectionPolicy(ProtectionPolicyBase):
    @odata(name="mailboxInclusionRules", navigation=True)
    @property
    def mailbox_inclusion_rules(self) -> EntityCollection[MailboxProtectionRule]:
        """Gets the mailboxInclusionRules property"""
        from office365.common.mailbox_protection_rule import MailboxProtectionRule

        return self.properties.get(
            "mailboxInclusionRules",
            EntityCollection[MailboxProtectionRule](
                self.context, MailboxProtectionRule, ResourcePath("mailboxInclusionRules", self.resource_path)
            ),
        )

    @odata(name="mailboxProtectionUnits", navigation=True)
    @property
    def mailbox_protection_units(self) -> EntityCollection[MailboxProtectionUnit]:
        """Gets the mailboxProtectionUnits property"""
        from office365.common.mailbox_protection_unit import MailboxProtectionUnit

        return self.properties.get(
            "mailboxProtectionUnits",
            EntityCollection[MailboxProtectionUnit](
                self.context, MailboxProtectionUnit, ResourcePath("mailboxProtectionUnits", self.resource_path)
            ),
        )

    @odata(name="mailboxProtectionUnitsBulkAdditionJobs", navigation=True)
    @property
    def mailbox_protection_units_bulk_addition_jobs(self) -> EntityCollection[MailboxProtectionUnitsBulkAdditionJob]:
        """Gets the mailboxProtectionUnitsBulkAdditionJobs property"""
        from office365.common.mailbox_protection_units_bulk_addition_job import (
            MailboxProtectionUnitsBulkAdditionJob,
        )

        return self.properties.get(
            "mailboxProtectionUnitsBulkAdditionJobs",
            EntityCollection[MailboxProtectionUnitsBulkAdditionJob](
                self.context,
                MailboxProtectionUnitsBulkAdditionJob,
                ResourcePath("mailboxProtectionUnitsBulkAdditionJobs", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExchangeProtectionPolicy"
