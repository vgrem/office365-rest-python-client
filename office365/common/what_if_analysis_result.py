from __future__ import annotations

from typing import Optional

from office365.directory.policies.conditionalaccess.whatifanalysisreasons import WhatIfAnalysisReasons
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class WhatIfAnalysisResult(Entity):
    @odata(name="analysisReasons")
    @property
    def analysis_reasons(self) -> WhatIfAnalysisReasons:
        """Gets the analysisReasons property"""
        return self.properties.get("analysisReasons", WhatIfAnalysisReasons.notSet)

    @odata(name="policyApplies")
    @property
    def policy_applies(self) -> Optional[bool]:
        """Gets the policyApplies property"""
        return self.properties.get("policyApplies", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WhatIfAnalysisResult"
