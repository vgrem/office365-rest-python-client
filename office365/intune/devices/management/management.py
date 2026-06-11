from office365.directory.rolemanagement.roles.permission import RolePermission
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.audit.event_collection import AuditEventCollection
from office365.intune.brand import IntuneBrand
from office365.intune.devices.category import DeviceCategory
from office365.intune.devices.enrollment.configuration import (
    DeviceEnrollmentConfiguration,
)
from office365.intune.devices.management.managed.managed import ManagedDevice
from office365.intune.devices.management.reports.reports import DeviceManagementReports
from office365.intune.devices.management.terms_and_conditions import TermsAndConditions
from office365.intune.devices.management.virtualendpoint.virtual_endpoint import VirtualEndpoint
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.odata_property import odata


class DeviceManagement(Entity):
    """
    The deviceManagement resource represents a tenant's collection device identities that have been pre-staged in
    Intune, and the enrollment profiles that may be assigned to device identities that support pre-enrollment
    configuration.
    """

    def get_effective_permissions(self, scope=None) -> ClientResult[ClientValueCollection[RolePermission]]:
        """Retrieves the effective permissions of the currently authenticated user"""
        return_type = ClientResult(self.context, ClientValueCollection(RolePermission))
        # params = {"scope": scope}
        qry = FunctionQuery(self, "getEffectivePermissions", None, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="auditEvents")
    @property
    def audit_events(self) -> AuditEventCollection:
        """"""
        return self.properties.get(
            "auditEvents",
            AuditEventCollection(self.context, ResourcePath("auditEvents", self.resource_path)),
        )

    @odata(name="virtualEndpoint")
    @property
    def virtual_endpoint(self) -> VirtualEndpoint:
        """"""
        return self.properties.get(
            "virtualEndpoint",
            VirtualEndpoint(self.context, ResourcePath("virtualEndpoint", self.resource_path)),
        )

    @odata(name="termsAndConditions")
    @property
    def terms_and_conditions(self) -> EntityCollection[TermsAndConditions]:
        """"""
        return self.properties.get(
            "termsAndConditions",
            EntityCollection(
                self.context,
                TermsAndConditions,
                ResourcePath("termsAndConditions", self.resource_path),
            ),
        )

    @odata(name="deviceCategories")
    @property
    def device_categories(self) -> EntityCollection[DeviceCategory]:
        """"""
        return self.properties.get(
            "deviceCategories",
            EntityCollection(
                self.context,
                DeviceCategory,
                ResourcePath("deviceCategories", self.resource_path),
            ),
        )

    @odata(name="deviceEnrollmentConfigurations")
    @property
    def device_enrollment_configurations(self) -> EntityCollection[DeviceEnrollmentConfiguration]:
        """"""
        return self.properties.get(
            "deviceEnrollmentConfigurations",
            EntityCollection(
                self.context,
                DeviceEnrollmentConfiguration,
                ResourcePath("deviceEnrollmentConfigurations", self.resource_path),
            ),
        )

    @odata(name="intuneBrand")
    @property
    def intune_brand(self) -> IntuneBrand:
        return self.properties.get("intuneBrand", IntuneBrand())

    @odata(name="managedDevices")
    @property
    def managed_devices(self) -> EntityCollection[ManagedDevice]:
        """"""
        return self.properties.get(
            "managedDevices",
            EntityCollection(
                self.context,
                ManagedDevice,
                ResourcePath("managedDevices", self.resource_path),
            ),
        )

    @property
    def reports(self) -> DeviceManagementReports:
        """"""
        return self.properties.get(
            "reports",
            DeviceManagementReports(self.context, ResourcePath("reports", self.resource_path)),
        )
