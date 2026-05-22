from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.migrationcenter.service.performance.throughput_data import (
    ThroughputData,
)


@dataclass
class PerformanceDashboardData(ClientValue):
    BottleneckList: StringCollection | None = None
    RecommendationList: StringCollection | None = None
    ThroughputTrend: ClientValueCollection[ThroughputData] | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.PerformanceDashboardData"
