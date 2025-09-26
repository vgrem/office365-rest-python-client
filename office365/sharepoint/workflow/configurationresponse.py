from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.workflow.configureduserinfo import ConfiguredUserInfo


class WorkflowConfigurationResponse(ClientValue):

    def __init__(
        self,
        approvers: ClientValueCollection[ConfiguredUserInfo] = ClientValueCollection(
            ConfiguredUserInfo
        ),
        category_id: str = None,
        category_name: str = None,
        configuration_id: int = None,
        country: str = None,
        e_sign_needed: bool = None,
        language: str = None,
        reviewers: ClientValueCollection[ConfiguredUserInfo] = ClientValueCollection(
            ConfiguredUserInfo
        ),
        source: str = None,
        type_: str = None,
    ):
        self.approvers = approvers
        self.category_id = category_id
        self.category_name = category_name
        self.configuration_id = configuration_id
        self.country = country
        self.e_sign_needed = e_sign_needed
        self.language = language
        self.reviewers = reviewers
        self.source = source
        self.type = type_
