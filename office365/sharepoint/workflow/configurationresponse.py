from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.workflow.configureduserinfo import ConfiguredUserInfo


@dataclass
class WorkflowConfigurationResponse(ClientValue):
    Approvers: ClientValueCollection[ConfiguredUserInfo] = field(
        default_factory=lambda: ClientValueCollection(ConfiguredUserInfo)
    )
    CategoryID: str | None = None
    CategoryName: str | None = None
    ConfigurationID: int | None = None
    Country: str | None = None
    ESignNeeded: bool | None = None
    Language: str | None = None
    Reviewers: ClientValueCollection[ConfiguredUserInfo] = field(
        default_factory=lambda: ClientValueCollection(ConfiguredUserInfo)
    )
    Source: str | None = None
    Type: str | None = None
