from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value
from office365.sharepoint.migrationcenter.service.performance.throughput_data import (
    ThroughputData,
)


@value
class PerformanceDashboardData(ClientValue):
    BottleneckList: StringCollection | None = None
    RecommendationList: StringCollection | None = None
    ThroughputTrend: ClientValueCollection[ThroughputData] = field(
        default_factory=lambda: ClientValueCollection(ThroughputData)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.PerformanceDashboardData"
