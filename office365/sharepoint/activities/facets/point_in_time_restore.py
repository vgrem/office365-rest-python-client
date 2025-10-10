from office365.runtime.client_value import ClientValue


class PointInTimeRestoreFacet(ClientValue):

    def __init__(self, restore_to_date_time: str = None):
        self.restoreToDateTime = restore_to_date_time

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.PointInTimeRestoreFacet"
