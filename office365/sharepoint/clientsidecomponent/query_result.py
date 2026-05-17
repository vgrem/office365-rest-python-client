from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPClientSideComponentQueryResult(ClientValue):
    """This object contains information about the requested component and the status of the query that was used to
    retrieve the component."""

    def __init__(
        self,
        component_type: Optional[str] = None,
        manifest: Optional[str] = None,
        manifest_type: Optional[str] = None,
        id_: Optional[str] = None,
        manifest_activated_time: Optional[datetime] = None,
        name: Optional[str] = None,
        status: Optional[int] = None,
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
