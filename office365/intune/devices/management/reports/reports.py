from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management_export_job import DeviceManagementExportJob


class DeviceManagementReports(Entity):
    """Device management reports entity"""

    @odata(name="exportJobs", navigation=True)
    @property
    def export_jobs(self) -> EntityCollection[DeviceManagementExportJob]:
        """Gets the exportJobs property"""
        from office365.intune.devices.management_export_job import (
            DeviceManagementExportJob,
        )

        return self.properties.get(
            "exportJobs",
            EntityCollection[DeviceManagementExportJob](
                self.context, DeviceManagementExportJob, ResourcePath("exportJobs", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementReports"

    def retrieve_device_app_installation_status_report(
        self,
        name: str,
        select: list[str],
        search: str,
        group_by: list[str],
        order_by: list[str],
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """retrieveDeviceAppInstallationStatusReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            search (str):
                search parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "retrieveDeviceAppInstallationStatusReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "search": search,
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_cached_report(
        self, id_: str, select: list[str], group_by: list[str], order_by: list[str], search: str, skip: int, top: int
    ) -> ClientResult[bytes]:
        """getCachedReport operation.

        Args:
            id_ (str):
                id parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getCachedReport",
            None,
            {
                "id": id_,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_compliance_policy_non_compliance_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getCompliancePolicyNonComplianceReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getCompliancePolicyNonComplianceReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_compliance_policy_non_compliance_summary_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getCompliancePolicyNonComplianceSummaryReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getCompliancePolicyNonComplianceSummaryReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_compliance_setting_non_compliance_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getComplianceSettingNonComplianceReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getComplianceSettingNonComplianceReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_configuration_policy_non_compliance_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getConfigurationPolicyNonComplianceReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getConfigurationPolicyNonComplianceReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_configuration_policy_non_compliance_summary_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getConfigurationPolicyNonComplianceSummaryReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getConfigurationPolicyNonComplianceSummaryReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_configuration_setting_non_compliance_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getConfigurationSettingNonComplianceReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getConfigurationSettingNonComplianceReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_device_management_intent_per_setting_contributing_profiles(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getDeviceManagementIntentPerSettingContributingProfiles operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getDeviceManagementIntentPerSettingContributingProfiles",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_device_management_intent_settings_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getDeviceManagementIntentSettingsReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getDeviceManagementIntentSettingsReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_device_non_compliance_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getDeviceNonComplianceReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getDeviceNonComplianceReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_devices_without_compliance_policy_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getDevicesWithoutCompliancePolicyReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getDevicesWithoutCompliancePolicyReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_historical_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getHistoricalReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getHistoricalReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_noncompliant_devices_and_settings_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getNoncompliantDevicesAndSettingsReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getNoncompliantDevicesAndSettingsReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_policy_non_compliance_metadata(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getPolicyNonComplianceMetadata operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getPolicyNonComplianceMetadata",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_policy_non_compliance_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getPolicyNonComplianceReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getPolicyNonComplianceReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_policy_non_compliance_summary_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getPolicyNonComplianceSummaryReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getPolicyNonComplianceSummaryReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_report_filters(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getReportFilters operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getReportFilters",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
            "DeviceManagementManagedDevices.Read.All",
            "DeviceManagementManagedDevices.ReadWrite.All",
        ],
    )
    def get_setting_non_compliance_report(
        self,
        name: str,
        select: list[str],
        group_by: list[str],
        order_by: list[str],
        search: str,
        skip: int,
        top: int,
        session_id: str,
        filter_: str,
    ) -> ClientResult[bytes]:
        """getSettingNonComplianceReport operation.

        Args:
            name (str):
                name parameter
            select (list[str]):
                select parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            search (str):
                search parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
            session_id (str):
                sessionId parameter
            filter_ (str):
                filter parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "getSettingNonComplianceReport",
            None,
            {
                "name": name,
                "select": StringCollection(select),
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "search": search,
                "skip": skip,
                "top": top,
                "sessionId": session_id,
                "filter": filter_,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
