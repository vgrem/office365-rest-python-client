from __future__ import annotations

from datetime import datetime

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserSignInInsight(Entity):
    @odata(name="lastSignInDateTime")
    @property
    def last_sign_in_date_time(self) -> datetime:
        """Gets the lastSignInDateTime property"""
        return self.properties.get("lastSignInDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserSignInInsight"
