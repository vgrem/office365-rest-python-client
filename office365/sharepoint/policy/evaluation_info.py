from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class PolicyEvaluationInfo(Entity):
    @odata(name="ApplicablePolicies")
    @property
    def applicable_policies(self) -> StringCollection:
        """Gets the ApplicablePolicies property"""
        return self.properties.get("ApplicablePolicies", StringCollection())

    @odata(name="DlpAccessScope")
    @property
    def dlp_access_scope(self) -> Optional[int]:
        """Gets the DlpAccessScope property"""
        return self.properties.get("DlpAccessScope", None)

    @odata(name="MatchedRules")
    @property
    def matched_rules(self) -> StringCollection:
        """Gets the MatchedRules property"""
        return self.properties.get("MatchedRules", StringCollection())

    @odata(name="OverriddenRules")
    @property
    def overridden_rules(self) -> StringCollection:
        """Gets the OverriddenRules property"""
        return self.properties.get("OverriddenRules", StringCollection())

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.PolicyEvaluationInfo"
