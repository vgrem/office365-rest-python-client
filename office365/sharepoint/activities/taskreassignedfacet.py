from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.activities.identity import ActivityIdentity


class TaskReassignedFacet(ClientValue):

    def __init__(
        self,
        assignees: ClientValueCollection[ActivityIdentity] = ClientValueCollection(
            ActivityIdentity
        ),
        previous_assignees: ClientValueCollection[
            ActivityIdentity
        ] = ClientValueCollection(ActivityIdentity),
        task_creator: ActivityIdentity = ActivityIdentity(),
    ):
        self.assignees = assignees
        self.previousAssignees = previous_assignees
        self.taskCreator = task_creator

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.TaskReassignedFacet"
