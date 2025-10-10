from office365.runtime.client_value import ClientValue


class AddToOneDriveFacet(ClientValue):
    """"""

    def __init__(
        self,
        added_datetime=None,
        mount_point_name=None,
        removed_datetime=None,
        added_date_time: str = None,
        removed_date_time: str = None,
    ):
        """
        :param str added_datetime:
        :param str mount_point_name:
        :param str removed_datetime:
        """
        self.addedDateTime = added_datetime
        self.mountPointName = (mount_point_name,)
        self.removedDateTime = removed_datetime
        self.addedDateTime = added_date_time
        self.removedDateTime = removed_date_time

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.AddToOneDriveFacet"
