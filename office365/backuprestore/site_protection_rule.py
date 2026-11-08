from __future__ import annotations

from typing import Optional

from office365.directory.protection.rules.base import ProtectionRuleBase
from office365.runtime.types.odata_property import odata


class SiteProtectionRule(ProtectionRuleBase):
    @odata(name="siteExpression")
    @property
    def site_expression(self) -> Optional[str]:
        """Gets the siteExpression property"""
        return self.properties.get("siteExpression", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SiteProtectionRule"
