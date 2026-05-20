from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.workflow.configureduserinfo import ConfiguredUserInfo


@dataclass
class WorkflowConfigurationResponse(ClientValue):
    approvers: ClientValueCollection[ConfiguredUserInfo] = field(
        default_factory=lambda: ClientValueCollection(ConfiguredUserInfo)
    )
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    configuration_id: Optional[int] = None
    country: Optional[str] = None
    e_sign_needed: Optional[bool] = None
    language: Optional[str] = None
    reviewers: ClientValueCollection[ConfiguredUserInfo] = field(
        default_factory=lambda: ClientValueCollection(ConfiguredUserInfo)
    )
    source: Optional[str] = None
    type: Optional[str] = None
