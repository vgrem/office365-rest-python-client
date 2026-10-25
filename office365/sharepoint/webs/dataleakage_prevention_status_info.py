from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SPDataLeakagePreventionStatusInfo(Entity):
    """"""

    @odata(name="ContainsConfidentialInfo")
    @property
    def contains_confidential_info(self) -> Optional[bool]:
        """Gets the ContainsConfidentialInfo property"""
        return self.properties.get("ContainsConfidentialInfo", None)

    @odata(name="ContainsConfidentialInfoLearnMoreUrl")
    @property
    def contains_confidential_info_learn_more_url(self) -> Optional[str]:
        """Gets the ContainsConfidentialInfoLearnMoreUrl property"""
        return self.properties.get("ContainsConfidentialInfoLearnMoreUrl", None)

    @odata(name="ExternalSharingTipsEnabled")
    @property
    def external_sharing_tips_enabled(self) -> Optional[bool]:
        """Gets the ExternalSharingTipsEnabled property"""
        return self.properties.get("ExternalSharingTipsEnabled", None)

    @odata(name="ExternalSharingTipsLearnMoreUrl")
    @property
    def external_sharing_tips_learn_more_url(self) -> Optional[str]:
        """Gets the ExternalSharingTipsLearnMoreUrl property"""
        return self.properties.get("ExternalSharingTipsLearnMoreUrl", None)
