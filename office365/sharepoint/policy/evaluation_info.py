from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class PolicyEvaluationInfo(Entity):
    @property
    def applicable_policies(self) -> StringCollection:
        """Gets the ApplicablePolicies property"""
        return self.properties.get("ApplicablePolicies", StringCollection())

    @property
    def dlp_access_scope(self) -> Optional[int]:
        """Gets the DlpAccessScope property"""
        return self.properties.get("DlpAccessScope", None)

    @property
    def matched_rules(self) -> StringCollection:
        """Gets the MatchedRules property"""
        return self.properties.get("MatchedRules", StringCollection())

    @property
    def overridden_rules(self) -> StringCollection:
        """Gets the OverriddenRules property"""
        return self.properties.get("OverriddenRules", StringCollection())

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.PolicyEvaluationInfo"
