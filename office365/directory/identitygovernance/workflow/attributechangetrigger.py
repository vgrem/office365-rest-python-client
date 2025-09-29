from office365.directory.identitygovernance.workflow.triggerattribute import (
    TriggerAttribute,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class AttributeChangeTrigger(ClientValue):

    def __init__(
        self,
        trigger_attributes: ClientValueCollection[
            TriggerAttribute
        ] = ClientValueCollection(TriggerAttribute),
    ):
        self.triggerAttributes = trigger_attributes
