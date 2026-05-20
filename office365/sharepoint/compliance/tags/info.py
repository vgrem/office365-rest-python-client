from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ComplianceTagInfo(ClientValue):
    """Compliance tag info

    is_record (bool): Is record
    is_regulatory (bool): Is regulatory
    should_keep (bool): Should keep
    tag_name (str): Tag name
    unified_rule_id (str): Unified rule id
    unified_tag_id (str): Unified tag id
    """

    IsRecord: Optional[bool] = None
    IsRegulatory: Optional[bool] = None
    ShouldKeep: Optional[bool] = None
    TagName: Optional[str] = None
    UnifiedRuleId: Optional[str] = None
    UnifiedTagId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.ComplianceFoundation.Models.ComplianceTagInfo"
