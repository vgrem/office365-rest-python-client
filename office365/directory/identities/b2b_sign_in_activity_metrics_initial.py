from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identities.b2b_sign_in_activity_metrics_base import B2BSignInActivityMetricsBase
from office365.runtime.types.odata_property import odata


class B2BSignInActivityMetricsInitial(B2BSignInActivityMetricsBase):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.B2BSignInActivityMetricsInitial"
