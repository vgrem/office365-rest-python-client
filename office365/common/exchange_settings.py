from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class ExchangeSettings(Entity):
    @odata(name="primaryMailboxId")
    @property
    def primary_mailbox_id(self) -> Optional[str]:
        """Gets the primaryMailboxId property"""
        return self.properties.get("primaryMailboxId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExchangeSettings"
