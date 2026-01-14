from office365.runtime.client_value import ClientValue


class GroupMoveOperation(ClientValue):
    def __init__(self, source_group: str = None, target_group: str = None):
        self.SourceGroup = source_group
        self.TargetGroup = target_group

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupMoveOperation"
