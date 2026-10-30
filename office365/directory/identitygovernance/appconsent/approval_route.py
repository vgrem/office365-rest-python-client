from office365.directory.identitygovernance.appconsent.request_collection import AppConsentRequestCollection
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AppConsentApprovalRoute(Entity):
    """
    Container for base resources that expose the app consent request API and features.
    Currently exposes only the appConsentRequests relationship.
    """

    @odata(name="appConsentRequests", navigation=True)
    @property
    def app_consent_requests(self):
        """A collection of appConsentRequest objects representing apps for which admin consent has been requested by
        one or more users."""
        return self.properties.get(
            "appConsentRequests",
            AppConsentRequestCollection(self.context, ResourcePath("appConsentRequests", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppConsentApprovalRoute"
