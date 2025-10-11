from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPClientSideComponentQueryResult(ClientValue):
    """This object contains information about the requested component and the status of the query that was used to
    retrieve the component."""

    def __init__(
        self,
        component_type: str = None,
        manifest: str = None,
        manifest_type: str = None,
        id_: str = None,
        manifest_activated_time: datetime = None,
        name: str = None,
        status: int = None,
    ):
        """
        :param str component_type: Specifies the type of component.
        :param str manifest:
        :param str manifest_type:
        """
        self.ComponentType = component_type
        self.Manifest = manifest
        self.ManifestType = manifest_type
        self.Id = id_
        self.ManifestActivatedTime = manifest_activated_time
        self.Name = name
        self.Status = status

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.SPClientSideComponentQueryResult"
