from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import key, odata


@key("stageNumber")
class DispositionReviewStage(Entity):
    """Represents a disposition review stage for a retention label."""

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="reviewersEmailAddresses")
    @property
    def reviewers_email_addresses(self) -> StringCollection:
        """Gets the reviewersEmailAddresses property"""
        return self.properties.get("reviewersEmailAddresses", StringCollection(None))

    @odata(name="stageNumber")
    @property
    def stage_number(self) -> Optional[str]:
        """Gets the stageNumber property"""
        return self.properties.get("stageNumber", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.DispositionReviewStage"
