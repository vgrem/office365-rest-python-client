from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class CopyToParams(ClientValue):
    AsNews: Optional[bool] = None
    AsPrivateAuthoringPage: Optional[bool] = None
    AsTemplate: Optional[bool] = None
    CanvasContentOnly: Optional[bool] = None
    ComponentJSONString: Optional[str] = None
    CreateCopyForEdit: Optional[bool] = None
    CreateCopyWithTitleSuffix: Optional[bool] = None
    CreateIfMissing: Optional[bool] = None
    DeleteSourcePage: Optional[bool] = None
    DependencyPropertyTypesToDeepCopy: ClientValueCollection[int] = field(
        default_factory=lambda: ClientValueCollection(int)
    )
    DestinationPageUniqueId: Optional[str] = None
    DestinationType: Optional[int] = None
    DestinationWebUrl: Optional[str] = None
    ScenarioID: Optional[int] = None
    ScenarioPayload: Optional[str] = None
    ShouldAddFallbackLinkForVideoForAmplify: Optional[bool] = None
    SitePageFlags: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CopyToParams"
