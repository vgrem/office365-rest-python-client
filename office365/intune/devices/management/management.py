from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from typing_extensions import Self

from office365.common.intune_brand import IntuneBrand
from office365.directory.rolemanagement.roles.permission import RolePermission
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.audit.event_collection import AuditEventCollection
from office365.intune.devices.category import DeviceCategory
from office365.intune.devices.enrollment.configuration import (
    DeviceEnrollmentConfiguration,
)
from office365.intune.devices.management.device_protection_overview import DeviceProtectionOverview
from office365.intune.devices.management.managed.collection import (
    ManagedDeviceCollection,
)
from office365.intune.devices.management.reports.reports import DeviceManagementReports
from office365.intune.devices.management.settings import DeviceManagementSettings
from office365.intune.devices.management.subscriptionstate import DeviceManagementSubscriptionState
from office365.intune.devices.management.terms_and_conditions import TermsAndConditions
from office365.intune.devices.management.user_experience_analytics_settings import UserExperienceAnalyticsSettings
from office365.intune.devices.management.virtualendpoint.virtual_endpoint import (
    VirtualEndpoint,
)
from office365.intune.devices.management.windows_malware_overview import WindowsMalwareOverview
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.group_policy_category import GroupPolicyCategory
    from office365.common.group_policy_configuration import GroupPolicyConfiguration
    from office365.common.group_policy_definition import GroupPolicyDefinition
    from office365.common.group_policy_definition_file import GroupPolicyDefinitionFile
    from office365.common.group_policy_migration_report import GroupPolicyMigrationReport
    from office365.common.group_policy_object_file import GroupPolicyObjectFile
    from office365.common.group_policy_uploaded_definition_file import GroupPolicyUploadedDefinitionFile
    from office365.common.role_definition import RoleDefinition
    from office365.intune.devices.and_app_management_assignment_filter import DeviceAndAppManagementAssignmentFilter
    from office365.intune.devices.and_app_management_role_assignment import (
        DeviceAndAppManagementRoleAssignment,
    )
    from office365.intune.devices.compliance.management_partner import (
        ComplianceManagementPartner,
    )
    from office365.intune.devices.compliance.policy import DeviceCompliancePolicy
    from office365.intune.devices.compliance_policy_device_state_summary import (
        DeviceCompliancePolicyDeviceStateSummary,
    )
    from office365.intune.devices.compliance_policy_setting_state_summary import (
        DeviceCompliancePolicySettingStateSummary,
    )
    from office365.intune.devices.configuration_device_state_summary import (
        DeviceConfigurationDeviceStateSummary,
    )
    from office365.intune.devices.configurations.configuration import (
        DeviceConfiguration,
    )
    from office365.intune.devices.management.apple_push_notification_certificate import (
        ApplePushNotificationCertificate,
    )
    from office365.intune.devices.management.detected_app import DetectedApp
    from office365.intune.devices.management.imported_windows_autopilot_device_identity import (
        ImportedWindowsAutopilotDeviceIdentity,
    )
    from office365.intune.devices.management.ios_update_device_status import IosUpdateDeviceStatus
    from office365.intune.devices.management.managed.device_overview import ManagedDeviceOverview
    from office365.intune.devices.management.managed.managed import ManagedDevice
    from office365.intune.devices.management.mobile_threat_defense_connector import (
        MobileThreatDefenseConnector,
    )
    from office365.intune.devices.management.mobileapps.mobile_app_troubleshooting_event import (
        MobileAppTroubleshootingEvent,
    )
    from office365.intune.devices.management.notification_message_template import (
        NotificationMessageTemplate,
    )
    from office365.intune.devices.management.on_premises_conditional_access_settings import (
        OnPremisesConditionalAccessSettings,
    )
    from office365.intune.devices.management.remoteassistance.partner import (
        RemoteAssistancePartner,
    )
    from office365.intune.devices.management.resource_operation import ResourceOperation
    from office365.intune.devices.management.software_update_status_summary import (
        SoftwareUpdateStatusSummary,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_app_performance_by_app_version_details import (  # noqa: E501
        UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDetails,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_app_performance_by_app_version_device_id import (  # noqa: E501
        UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDeviceId,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_app_performance_by_os_version import (  # noqa: E501
        UserExperienceAnalyticsAppHealthAppPerformanceByOSVersion,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_application_performance import (  # noqa: E501
        UserExperienceAnalyticsAppHealthApplicationPerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_device_model_performance import (  # noqa: E501
        UserExperienceAnalyticsAppHealthDeviceModelPerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_device_performance import (  # noqa: E501
        UserExperienceAnalyticsAppHealthDevicePerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_device_performance_details import (  # noqa: E501
        UserExperienceAnalyticsAppHealthDevicePerformanceDetails,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_os_version_performance import (  # noqa: E501
        UserExperienceAnalyticsAppHealthOSVersionPerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_baseline import (
        UserExperienceAnalyticsBaseline,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_category import (
        UserExperienceAnalyticsCategory,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_performance import (  # noqa: E501
        UserExperienceAnalyticsDevicePerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_scores import (
        UserExperienceAnalyticsDeviceScores,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_startup_history import (  # noqa: E501
        UserExperienceAnalyticsDeviceStartupHistory,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_startup_process import (  # noqa: E501
        UserExperienceAnalyticsDeviceStartupProcess,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_startup_process_performance import (  # noqa: E501
        UserExperienceAnalyticsDeviceStartupProcessPerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_metric_history import (
        UserExperienceAnalyticsMetricHistory,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_model_scores import (
        UserExperienceAnalyticsModelScores,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_overview import (
        UserExperienceAnalyticsOverview,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_score_history import (
        UserExperienceAnalyticsScoreHistory,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_devices_summary import (  # noqa: E501
        UserExperienceAnalyticsWorkFromAnywhereDevicesSummary,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_hardware_readiness_metric import (  # noqa: E501
        UserExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_metric import (  # noqa: E501
        UserExperienceAnalyticsWorkFromAnywhereMetric,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_model_performance import (  # noqa: E501
        UserExperienceAnalyticsWorkFromAnywhereModelPerformance,
    )
    from office365.intune.devices.management.windows_autopilot_deployment_profile import (
        WindowsAutopilotDeploymentProfile,
    )
    from office365.intune.devices.management.windows_autopilot_device_identity import (
        WindowsAutopilotDeviceIdentity,
    )
    from office365.intune.devices.management.windows_information_protection_app_learning_summary import (
        WindowsInformationProtectionAppLearningSummary,
    )
    from office365.intune.devices.management.windows_information_protection_network_learning_summary import (
        WindowsInformationProtectionNetworkLearningSummary,
    )
    from office365.intune.devices.management.windowsmalware.windows_malware_information import WindowsMalwareInformation
    from office365.intune.devices.management_compliance_policy import DeviceManagementCompliancePolicy
    from office365.intune.devices.management_configuration_category import DeviceManagementConfigurationCategory
    from office365.intune.devices.management_configuration_policy import DeviceManagementConfigurationPolicy
    from office365.intune.devices.management_configuration_policy_template import (
        DeviceManagementConfigurationPolicyTemplate,
    )
    from office365.intune.devices.management_configuration_setting_definition import (
        DeviceManagementConfigurationSettingDefinition,
    )
    from office365.intune.devices.management_configuration_setting_template import (
        DeviceManagementConfigurationSettingTemplate,
    )
    from office365.intune.devices.management_exchange_connector import (
        DeviceManagementExchangeConnector,
    )
    from office365.intune.devices.management_partner import DeviceManagementPartner
    from office365.intune.devices.management_reusable_policy_setting import DeviceManagementReusablePolicySetting
    from office365.intune.devices.management_troubleshooting_event import (
        DeviceManagementTroubleshootingEvent,
    )


class DeviceManagement(Entity):
    """
    The deviceManagement resource represents a tenant's collection device identities that have been pre-staged in
    Intune, and the enrollment profiles that may be assigned to device identities that support pre-enrollment
    configuration.
    """

    @require_permission(
        delegated=["DeviceManagementRBAC.Read.All"],
        application=["DeviceManagementRBAC.Read.All"],
    )
    def get_effective_permissions(self, scope=None) -> ClientResult[ClientValueCollection[RolePermission]]:
        """Retrieves the effective permissions of the currently authenticated user"""
        return_type = ClientResult(self.context, ClientValueCollection(RolePermission))
        # params = {"scope": scope}
        qry = FunctionQuery(self, "getEffectivePermissions", None, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="auditEvents", navigation=True)
    @property
    def audit_events(self) -> AuditEventCollection:
        """"""
        return self.properties.get(
            "auditEvents",
            AuditEventCollection(self.context, ResourcePath("auditEvents", self.resource_path)),
        )

    @odata(name="virtualEndpoint", navigation=True)
    @property
    def virtual_endpoint(self) -> VirtualEndpoint:
        """"""
        return self.properties.get(
            "virtualEndpoint",
            VirtualEndpoint(self.context, ResourcePath("virtualEndpoint", self.resource_path)),
        )

    @odata(name="termsAndConditions", navigation=True)
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

    @odata(name="deviceCategories", navigation=True)
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

    @odata(name="deviceEnrollmentConfigurations", navigation=True)
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

    @odata(name="managedDevices", navigation=True)
    @property
    def managed_devices(self) -> ManagedDeviceCollection:
        """"""
        return self.properties.get(
            "managedDevices",
            ManagedDeviceCollection(
                self.context,
                ResourcePath("managedDevices", self.resource_path),
            ),
        )

    @odata(name="reports", navigation=True)
    @property
    def reports(self) -> DeviceManagementReports:
        """"""
        return self.properties.get(
            "reports",
            DeviceManagementReports(self.context, ResourcePath("reports", self.resource_path)),
        )

    @odata(name="intuneAccountId")
    @property
    def intune_account_id(self) -> Optional[UUID]:
        """Gets the intuneAccountId property"""
        return self.properties.get("intuneAccountId", None)

    @odata(name="settings")
    @property
    def settings(self) -> DeviceManagementSettings:
        """Gets the settings property"""
        return self.properties.get("settings", DeviceManagementSettings())

    @odata(name="deviceProtectionOverview")
    @property
    def device_protection_overview(self) -> DeviceProtectionOverview:
        """Gets the deviceProtectionOverview property"""
        return self.properties.get("deviceProtectionOverview", DeviceProtectionOverview())

    @odata(name="subscriptionState")
    @property
    def subscription_state(self) -> DeviceManagementSubscriptionState:
        """Gets the subscriptionState property"""
        return self.properties.get("subscriptionState", DeviceManagementSubscriptionState.pending)

    @odata(name="userExperienceAnalyticsSettings")
    @property
    def user_experience_analytics_settings(self) -> UserExperienceAnalyticsSettings:
        """Gets the userExperienceAnalyticsSettings property"""
        return self.properties.get("userExperienceAnalyticsSettings", UserExperienceAnalyticsSettings())

    @odata(name="windowsMalwareOverview")
    @property
    def windows_malware_overview(self) -> WindowsMalwareOverview:
        """Gets the windowsMalwareOverview property"""
        return self.properties.get("windowsMalwareOverview", WindowsMalwareOverview())

    @odata(name="deviceCompliancePolicies", navigation=True)
    @property
    def device_compliance_policies(self) -> EntityCollection[DeviceCompliancePolicy]:
        """Gets the deviceCompliancePolicies property"""
        from office365.intune.devices.compliance.policy import DeviceCompliancePolicy

        return self.properties.get(
            "deviceCompliancePolicies",
            EntityCollection[DeviceCompliancePolicy](
                self.context, DeviceCompliancePolicy, ResourcePath("deviceCompliancePolicies", self.resource_path)
            ),
        )

    @odata(name="deviceCompliancePolicyDeviceStateSummary", navigation=True)
    @property
    def device_compliance_policy_device_state_summary(self) -> DeviceCompliancePolicyDeviceStateSummary:
        """Gets the deviceCompliancePolicyDeviceStateSummary property"""
        from office365.intune.devices.compliance_policy_device_state_summary import (
            DeviceCompliancePolicyDeviceStateSummary,
        )

        return self.properties.get(
            "deviceCompliancePolicyDeviceStateSummary",
            DeviceCompliancePolicyDeviceStateSummary(
                self.context, ResourcePath("deviceCompliancePolicyDeviceStateSummary", self.resource_path)
            ),
        )

    @odata(name="deviceCompliancePolicySettingStateSummaries", navigation=True)
    @property
    def device_compliance_policy_setting_state_summaries(
        self,
    ) -> EntityCollection[DeviceCompliancePolicySettingStateSummary]:
        """Gets the deviceCompliancePolicySettingStateSummaries property"""
        from office365.intune.devices.compliance_policy_setting_state_summary import (
            DeviceCompliancePolicySettingStateSummary,
        )

        return self.properties.get(
            "deviceCompliancePolicySettingStateSummaries",
            EntityCollection[DeviceCompliancePolicySettingStateSummary](
                self.context,
                DeviceCompliancePolicySettingStateSummary,
                ResourcePath("deviceCompliancePolicySettingStateSummaries", self.resource_path),
            ),
        )

    @odata(name="deviceConfigurationDeviceStateSummaries", navigation=True)
    @property
    def device_configuration_device_state_summaries(self) -> DeviceConfigurationDeviceStateSummary:
        """Gets the deviceConfigurationDeviceStateSummaries property"""
        from office365.intune.devices.configuration_device_state_summary import (
            DeviceConfigurationDeviceStateSummary,
        )

        return self.properties.get(
            "deviceConfigurationDeviceStateSummaries",
            DeviceConfigurationDeviceStateSummary(
                self.context, ResourcePath("deviceConfigurationDeviceStateSummaries", self.resource_path)
            ),
        )

    @odata(name="deviceConfigurations", navigation=True)
    @property
    def device_configurations(self) -> EntityCollection[DeviceConfiguration]:
        """Gets the deviceConfigurations property"""
        from office365.intune.devices.configurations.configuration import (
            DeviceConfiguration,
        )

        return self.properties.get(
            "deviceConfigurations",
            EntityCollection[DeviceConfiguration](
                self.context, DeviceConfiguration, ResourcePath("deviceConfigurations", self.resource_path)
            ),
        )

    @odata(name="iosUpdateStatuses", navigation=True)
    @property
    def ios_update_statuses(self) -> EntityCollection[IosUpdateDeviceStatus]:
        """Gets the iosUpdateStatuses property"""
        from office365.intune.devices.management.ios_update_device_status import IosUpdateDeviceStatus

        return self.properties.get(
            "iosUpdateStatuses",
            EntityCollection[IosUpdateDeviceStatus](
                self.context, IosUpdateDeviceStatus, ResourcePath("iosUpdateStatuses", self.resource_path)
            ),
        )

    @odata(name="softwareUpdateStatusSummary", navigation=True)
    @property
    def software_update_status_summary(self) -> SoftwareUpdateStatusSummary:
        """Gets the softwareUpdateStatusSummary property"""
        from office365.intune.devices.management.software_update_status_summary import (
            SoftwareUpdateStatusSummary,
        )

        return self.properties.get(
            "softwareUpdateStatusSummary",
            SoftwareUpdateStatusSummary(self.context, ResourcePath("softwareUpdateStatusSummary", self.resource_path)),
        )

    @odata(name="complianceManagementPartners", navigation=True)
    @property
    def compliance_management_partners(self) -> EntityCollection[ComplianceManagementPartner]:
        """Gets the complianceManagementPartners property"""
        from office365.intune.devices.compliance.management_partner import (
            ComplianceManagementPartner,
        )

        return self.properties.get(
            "complianceManagementPartners",
            EntityCollection[ComplianceManagementPartner](
                self.context,
                ComplianceManagementPartner,
                ResourcePath("complianceManagementPartners", self.resource_path),
            ),
        )

    @odata(name="conditionalAccessSettings", navigation=True)
    @property
    def conditional_access_settings(self) -> OnPremisesConditionalAccessSettings:
        """Gets the conditionalAccessSettings property"""
        from office365.intune.devices.management.on_premises_conditional_access_settings import (
            OnPremisesConditionalAccessSettings,
        )

        return self.properties.get(
            "conditionalAccessSettings",
            OnPremisesConditionalAccessSettings(
                self.context, ResourcePath("conditionalAccessSettings", self.resource_path)
            ),
        )

    @odata(name="deviceManagementPartners", navigation=True)
    @property
    def device_management_partners(self) -> EntityCollection[DeviceManagementPartner]:
        """Gets the deviceManagementPartners property"""
        from office365.intune.devices.management_partner import DeviceManagementPartner

        return self.properties.get(
            "deviceManagementPartners",
            EntityCollection[DeviceManagementPartner](
                self.context, DeviceManagementPartner, ResourcePath("deviceManagementPartners", self.resource_path)
            ),
        )

    @odata(name="exchangeConnectors", navigation=True)
    @property
    def exchange_connectors(self) -> EntityCollection[DeviceManagementExchangeConnector]:
        """Gets the exchangeConnectors property"""
        from office365.intune.devices.management_exchange_connector import (
            DeviceManagementExchangeConnector,
        )

        return self.properties.get(
            "exchangeConnectors",
            EntityCollection[DeviceManagementExchangeConnector](
                self.context, DeviceManagementExchangeConnector, ResourcePath("exchangeConnectors", self.resource_path)
            ),
        )

    @odata(name="mobileThreatDefenseConnectors", navigation=True)
    @property
    def mobile_threat_defense_connectors(self) -> EntityCollection[MobileThreatDefenseConnector]:
        """Gets the mobileThreatDefenseConnectors property"""
        from office365.intune.devices.management.mobile_threat_defense_connector import (
            MobileThreatDefenseConnector,
        )

        return self.properties.get(
            "mobileThreatDefenseConnectors",
            EntityCollection[MobileThreatDefenseConnector](
                self.context,
                MobileThreatDefenseConnector,
                ResourcePath("mobileThreatDefenseConnectors", self.resource_path),
            ),
        )

    @odata(name="applePushNotificationCertificate", navigation=True)
    @property
    def apple_push_notification_certificate(self) -> ApplePushNotificationCertificate:
        """Gets the applePushNotificationCertificate property"""
        from office365.intune.devices.management.apple_push_notification_certificate import (
            ApplePushNotificationCertificate,
        )

        return self.properties.get(
            "applePushNotificationCertificate",
            ApplePushNotificationCertificate(
                self.context, ResourcePath("applePushNotificationCertificate", self.resource_path)
            ),
        )

    @odata(name="detectedApps", navigation=True)
    @property
    def detected_apps(self) -> EntityCollection[DetectedApp]:
        """Gets the detectedApps property"""
        from office365.intune.devices.management.detected_app import DetectedApp

        return self.properties.get(
            "detectedApps",
            EntityCollection[DetectedApp](self.context, DetectedApp, ResourcePath("detectedApps", self.resource_path)),
        )

    @odata(name="managedDeviceOverview", navigation=True)
    @property
    def managed_device_overview(self) -> ManagedDeviceOverview:
        """Gets the managedDeviceOverview property"""
        from office365.intune.devices.management.managed.device_overview import ManagedDeviceOverview

        return self.properties.get(
            "managedDeviceOverview",
            ManagedDeviceOverview(self.context, ResourcePath("managedDeviceOverview", self.resource_path)),
        )

    @odata(name="mobileAppTroubleshootingEvents", navigation=True)
    @property
    def mobile_app_troubleshooting_events(self) -> EntityCollection[MobileAppTroubleshootingEvent]:
        """Gets the mobileAppTroubleshootingEvents property"""
        from office365.intune.devices.management.mobileapps.mobile_app_troubleshooting_event import (
            MobileAppTroubleshootingEvent,
        )

        return self.properties.get(
            "mobileAppTroubleshootingEvents",
            EntityCollection[MobileAppTroubleshootingEvent](
                self.context,
                MobileAppTroubleshootingEvent,
                ResourcePath("mobileAppTroubleshootingEvents", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthApplicationPerformance", navigation=True)
    @property
    def user_experience_analytics_app_health_application_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAppHealthApplicationPerformance]:
        """Gets the userExperienceAnalyticsAppHealthApplicationPerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_application_performance import (  # noqa: E501
            UserExperienceAnalyticsAppHealthApplicationPerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthApplicationPerformance",
            EntityCollection[UserExperienceAnalyticsAppHealthApplicationPerformance](
                self.context,
                UserExperienceAnalyticsAppHealthApplicationPerformance,
                ResourcePath("userExperienceAnalyticsAppHealthApplicationPerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDetails", navigation=True)
    @property
    def user_experience_analytics_app_health_application_performance_by_app_version_details(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDetails]:
        """Gets the userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDetails property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_app_performance_by_app_version_details import (  # noqa: E501
            UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDetails,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDetails",
            EntityCollection[UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDetails](
                self.context,
                UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDetails,
                ResourcePath(
                    "userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDetails", self.resource_path
                ),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDeviceId", navigation=True)
    @property
    def user_experience_analytics_app_health_application_performance_by_app_version_device_id(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDeviceId]:
        """Gets the userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDeviceId property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_app_performance_by_app_version_device_id import (  # noqa: E501
            UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDeviceId,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDeviceId",
            EntityCollection[UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDeviceId](
                self.context,
                UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDeviceId,
                ResourcePath(
                    "userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDeviceId", self.resource_path
                ),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthApplicationPerformanceByOSVersion", navigation=True)
    @property
    def user_experience_analytics_app_health_application_performance_by_os_version(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAppHealthAppPerformanceByOSVersion]:
        """Gets the userExperienceAnalyticsAppHealthApplicationPerformanceByOSVersion property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_app_performance_by_os_version import (  # noqa: E501
            UserExperienceAnalyticsAppHealthAppPerformanceByOSVersion,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthApplicationPerformanceByOSVersion",
            EntityCollection[UserExperienceAnalyticsAppHealthAppPerformanceByOSVersion](
                self.context,
                UserExperienceAnalyticsAppHealthAppPerformanceByOSVersion,
                ResourcePath("userExperienceAnalyticsAppHealthApplicationPerformanceByOSVersion", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthDeviceModelPerformance", navigation=True)
    @property
    def user_experience_analytics_app_health_device_model_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAppHealthDeviceModelPerformance]:
        """Gets the userExperienceAnalyticsAppHealthDeviceModelPerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_device_model_performance import (  # noqa: E501
            UserExperienceAnalyticsAppHealthDeviceModelPerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthDeviceModelPerformance",
            EntityCollection[UserExperienceAnalyticsAppHealthDeviceModelPerformance](
                self.context,
                UserExperienceAnalyticsAppHealthDeviceModelPerformance,
                ResourcePath("userExperienceAnalyticsAppHealthDeviceModelPerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthDevicePerformance", navigation=True)
    @property
    def user_experience_analytics_app_health_device_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAppHealthDevicePerformance]:
        """Gets the userExperienceAnalyticsAppHealthDevicePerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_device_performance import (  # noqa: E501
            UserExperienceAnalyticsAppHealthDevicePerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthDevicePerformance",
            EntityCollection[UserExperienceAnalyticsAppHealthDevicePerformance](
                self.context,
                UserExperienceAnalyticsAppHealthDevicePerformance,
                ResourcePath("userExperienceAnalyticsAppHealthDevicePerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthDevicePerformanceDetails", navigation=True)
    @property
    def user_experience_analytics_app_health_device_performance_details(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAppHealthDevicePerformanceDetails]:
        """Gets the userExperienceAnalyticsAppHealthDevicePerformanceDetails property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_device_performance_details import (  # noqa: E501
            UserExperienceAnalyticsAppHealthDevicePerformanceDetails,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthDevicePerformanceDetails",
            EntityCollection[UserExperienceAnalyticsAppHealthDevicePerformanceDetails](
                self.context,
                UserExperienceAnalyticsAppHealthDevicePerformanceDetails,
                ResourcePath("userExperienceAnalyticsAppHealthDevicePerformanceDetails", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthOSVersionPerformance", navigation=True)
    @property
    def user_experience_analytics_app_health_os_version_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAppHealthOSVersionPerformance]:
        """Gets the userExperienceAnalyticsAppHealthOSVersionPerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_os_version_performance import (  # noqa: E501
            UserExperienceAnalyticsAppHealthOSVersionPerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthOSVersionPerformance",
            EntityCollection[UserExperienceAnalyticsAppHealthOSVersionPerformance](
                self.context,
                UserExperienceAnalyticsAppHealthOSVersionPerformance,
                ResourcePath("userExperienceAnalyticsAppHealthOSVersionPerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthOverview", navigation=True)
    @property
    def user_experience_analytics_app_health_overview(self) -> UserExperienceAnalyticsCategory:
        """Gets the userExperienceAnalyticsAppHealthOverview property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_category import (
            UserExperienceAnalyticsCategory,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthOverview",
            UserExperienceAnalyticsCategory(
                self.context, ResourcePath("userExperienceAnalyticsAppHealthOverview", self.resource_path)
            ),
        )

    @odata(name="userExperienceAnalyticsBaselines", navigation=True)
    @property
    def user_experience_analytics_baselines(self) -> EntityCollection[UserExperienceAnalyticsBaseline]:
        """Gets the userExperienceAnalyticsBaselines property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_baseline import (
            UserExperienceAnalyticsBaseline,
        )

        return self.properties.get(
            "userExperienceAnalyticsBaselines",
            EntityCollection[UserExperienceAnalyticsBaseline](
                self.context,
                UserExperienceAnalyticsBaseline,
                ResourcePath("userExperienceAnalyticsBaselines", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsCategories", navigation=True)
    @property
    def user_experience_analytics_categories(self) -> EntityCollection[UserExperienceAnalyticsCategory]:
        """Gets the userExperienceAnalyticsCategories property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_category import (
            UserExperienceAnalyticsCategory,
        )

        return self.properties.get(
            "userExperienceAnalyticsCategories",
            EntityCollection[UserExperienceAnalyticsCategory](
                self.context,
                UserExperienceAnalyticsCategory,
                ResourcePath("userExperienceAnalyticsCategories", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsDevicePerformance", navigation=True)
    @property
    def user_experience_analytics_device_performance(self) -> EntityCollection[UserExperienceAnalyticsDevicePerformance]:
        """Gets the userExperienceAnalyticsDevicePerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_performance import (  # noqa: E501
            UserExperienceAnalyticsDevicePerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsDevicePerformance",
            EntityCollection[UserExperienceAnalyticsDevicePerformance](
                self.context,
                UserExperienceAnalyticsDevicePerformance,
                ResourcePath("userExperienceAnalyticsDevicePerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsDeviceScores", navigation=True)
    @property
    def user_experience_analytics_device_scores(self) -> EntityCollection[UserExperienceAnalyticsDeviceScores]:
        """Gets the userExperienceAnalyticsDeviceScores property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_scores import (
            UserExperienceAnalyticsDeviceScores,
        )

        return self.properties.get(
            "userExperienceAnalyticsDeviceScores",
            EntityCollection[UserExperienceAnalyticsDeviceScores](
                self.context,
                UserExperienceAnalyticsDeviceScores,
                ResourcePath("userExperienceAnalyticsDeviceScores", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsDeviceStartupHistory", navigation=True)
    @property
    def user_experience_analytics_device_startup_history(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsDeviceStartupHistory]:
        """Gets the userExperienceAnalyticsDeviceStartupHistory property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_startup_history import (  # noqa: E501
            UserExperienceAnalyticsDeviceStartupHistory,
        )

        return self.properties.get(
            "userExperienceAnalyticsDeviceStartupHistory",
            EntityCollection[UserExperienceAnalyticsDeviceStartupHistory](
                self.context,
                UserExperienceAnalyticsDeviceStartupHistory,
                ResourcePath("userExperienceAnalyticsDeviceStartupHistory", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsDeviceStartupProcesses", navigation=True)
    @property
    def user_experience_analytics_device_startup_processes(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsDeviceStartupProcess]:
        """Gets the userExperienceAnalyticsDeviceStartupProcesses property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_startup_process import (  # noqa: E501
            UserExperienceAnalyticsDeviceStartupProcess,
        )

        return self.properties.get(
            "userExperienceAnalyticsDeviceStartupProcesses",
            EntityCollection[UserExperienceAnalyticsDeviceStartupProcess](
                self.context,
                UserExperienceAnalyticsDeviceStartupProcess,
                ResourcePath("userExperienceAnalyticsDeviceStartupProcesses", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsDeviceStartupProcessPerformance", navigation=True)
    @property
    def user_experience_analytics_device_startup_process_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsDeviceStartupProcessPerformance]:
        """Gets the userExperienceAnalyticsDeviceStartupProcessPerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_startup_process_performance import (  # noqa: E501
            UserExperienceAnalyticsDeviceStartupProcessPerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsDeviceStartupProcessPerformance",
            EntityCollection[UserExperienceAnalyticsDeviceStartupProcessPerformance](
                self.context,
                UserExperienceAnalyticsDeviceStartupProcessPerformance,
                ResourcePath("userExperienceAnalyticsDeviceStartupProcessPerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsMetricHistory", navigation=True)
    @property
    def user_experience_analytics_metric_history(self) -> EntityCollection[UserExperienceAnalyticsMetricHistory]:
        """Gets the userExperienceAnalyticsMetricHistory property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_metric_history import (  # noqa: E501
            UserExperienceAnalyticsMetricHistory,
        )

        return self.properties.get(
            "userExperienceAnalyticsMetricHistory",
            EntityCollection[UserExperienceAnalyticsMetricHistory](
                self.context,
                UserExperienceAnalyticsMetricHistory,
                ResourcePath("userExperienceAnalyticsMetricHistory", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsModelScores", navigation=True)
    @property
    def user_experience_analytics_model_scores(self) -> EntityCollection[UserExperienceAnalyticsModelScores]:
        """Gets the userExperienceAnalyticsModelScores property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_model_scores import (
            UserExperienceAnalyticsModelScores,
        )

        return self.properties.get(
            "userExperienceAnalyticsModelScores",
            EntityCollection[UserExperienceAnalyticsModelScores](
                self.context,
                UserExperienceAnalyticsModelScores,
                ResourcePath("userExperienceAnalyticsModelScores", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsOverview", navigation=True)
    @property
    def user_experience_analytics_overview(self) -> UserExperienceAnalyticsOverview:
        """Gets the userExperienceAnalyticsOverview property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_overview import (
            UserExperienceAnalyticsOverview,
        )

        return self.properties.get(
            "userExperienceAnalyticsOverview",
            UserExperienceAnalyticsOverview(
                self.context, ResourcePath("userExperienceAnalyticsOverview", self.resource_path)
            ),
        )

    @odata(name="userExperienceAnalyticsScoreHistory", navigation=True)
    @property
    def user_experience_analytics_score_history(self) -> EntityCollection[UserExperienceAnalyticsScoreHistory]:
        """Gets the userExperienceAnalyticsScoreHistory property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_score_history import (
            UserExperienceAnalyticsScoreHistory,
        )

        return self.properties.get(
            "userExperienceAnalyticsScoreHistory",
            EntityCollection[UserExperienceAnalyticsScoreHistory](
                self.context,
                UserExperienceAnalyticsScoreHistory,
                ResourcePath("userExperienceAnalyticsScoreHistory", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric", navigation=True)
    @property
    def user_experience_analytics_work_from_anywhere_hardware_readiness_metric(
        self,
    ) -> UserExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric:
        """Gets the userExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_hardware_readiness_metric import (  # noqa: E501
            UserExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric,
        )

        return self.properties.get(
            "userExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric",
            UserExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric(
                self.context,
                ResourcePath("userExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsWorkFromAnywhereMetrics", navigation=True)
    @property
    def user_experience_analytics_work_from_anywhere_metrics(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsWorkFromAnywhereMetric]:
        """Gets the userExperienceAnalyticsWorkFromAnywhereMetrics property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_metric import (  # noqa: E501
            UserExperienceAnalyticsWorkFromAnywhereMetric,
        )

        return self.properties.get(
            "userExperienceAnalyticsWorkFromAnywhereMetrics",
            EntityCollection[UserExperienceAnalyticsWorkFromAnywhereMetric](
                self.context,
                UserExperienceAnalyticsWorkFromAnywhereMetric,
                ResourcePath("userExperienceAnalyticsWorkFromAnywhereMetrics", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsWorkFromAnywhereModelPerformance", navigation=True)
    @property
    def user_experience_analytics_work_from_anywhere_model_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsWorkFromAnywhereModelPerformance]:
        """Gets the userExperienceAnalyticsWorkFromAnywhereModelPerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_model_performance import (  # noqa: E501
            UserExperienceAnalyticsWorkFromAnywhereModelPerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsWorkFromAnywhereModelPerformance",
            EntityCollection[UserExperienceAnalyticsWorkFromAnywhereModelPerformance](
                self.context,
                UserExperienceAnalyticsWorkFromAnywhereModelPerformance,
                ResourcePath("userExperienceAnalyticsWorkFromAnywhereModelPerformance", self.resource_path),
            ),
        )

    @odata(name="windowsMalwareInformation", navigation=True)
    @property
    def windows_malware_information(self) -> EntityCollection[WindowsMalwareInformation]:
        """Gets the windowsMalwareInformation property"""
        from office365.intune.devices.management.windowsmalware.windows_malware_information import (
            WindowsMalwareInformation,
        )

        return self.properties.get(
            "windowsMalwareInformation",
            EntityCollection[WindowsMalwareInformation](
                self.context, WindowsMalwareInformation, ResourcePath("windowsMalwareInformation", self.resource_path)
            ),
        )

    @odata(name="importedWindowsAutopilotDeviceIdentities", navigation=True)
    @property
    def imported_windows_autopilot_device_identities(self) -> EntityCollection[ImportedWindowsAutopilotDeviceIdentity]:
        """Gets the importedWindowsAutopilotDeviceIdentities property"""
        from office365.intune.devices.management.imported_windows_autopilot_device_identity import (
            ImportedWindowsAutopilotDeviceIdentity,
        )

        return self.properties.get(
            "importedWindowsAutopilotDeviceIdentities",
            EntityCollection[ImportedWindowsAutopilotDeviceIdentity](
                self.context,
                ImportedWindowsAutopilotDeviceIdentity,
                ResourcePath("importedWindowsAutopilotDeviceIdentities", self.resource_path),
            ),
        )

    @odata(name="windowsAutopilotDeviceIdentities", navigation=True)
    @property
    def windows_autopilot_device_identities(self) -> EntityCollection[WindowsAutopilotDeviceIdentity]:
        """Gets the windowsAutopilotDeviceIdentities property"""
        from office365.intune.devices.management.windows_autopilot_device_identity import (
            WindowsAutopilotDeviceIdentity,
        )

        return self.properties.get(
            "windowsAutopilotDeviceIdentities",
            EntityCollection[WindowsAutopilotDeviceIdentity](
                self.context,
                WindowsAutopilotDeviceIdentity,
                ResourcePath("windowsAutopilotDeviceIdentities", self.resource_path),
            ),
        )

    @odata(name="notificationMessageTemplates", navigation=True)
    @property
    def notification_message_templates(self) -> EntityCollection[NotificationMessageTemplate]:
        """Gets the notificationMessageTemplates property"""
        from office365.intune.devices.management.notification_message_template import (
            NotificationMessageTemplate,
        )

        return self.properties.get(
            "notificationMessageTemplates",
            EntityCollection[NotificationMessageTemplate](
                self.context,
                NotificationMessageTemplate,
                ResourcePath("notificationMessageTemplates", self.resource_path),
            ),
        )

    @odata(name="resourceOperations", navigation=True)
    @property
    def resource_operations(self) -> EntityCollection[ResourceOperation]:
        """Gets the resourceOperations property"""
        from office365.intune.devices.management.resource_operation import (
            ResourceOperation,
        )

        return self.properties.get(
            "resourceOperations",
            EntityCollection[ResourceOperation](
                self.context, ResourceOperation, ResourcePath("resourceOperations", self.resource_path)
            ),
        )

    @odata(name="roleAssignments", navigation=True)
    @property
    def role_assignments(self) -> EntityCollection[DeviceAndAppManagementRoleAssignment]:
        """Gets the roleAssignments property"""
        from office365.intune.devices.and_app_management_role_assignment import (
            DeviceAndAppManagementRoleAssignment,
        )

        return self.properties.get(
            "roleAssignments",
            EntityCollection[DeviceAndAppManagementRoleAssignment](
                self.context, DeviceAndAppManagementRoleAssignment, ResourcePath("roleAssignments", self.resource_path)
            ),
        )

    @odata(name="roleDefinitions", navigation=True)
    @property
    def role_definitions(self) -> EntityCollection[RoleDefinition]:
        """Gets the roleDefinitions property"""
        from office365.common.role_definition import RoleDefinition

        return self.properties.get(
            "roleDefinitions",
            EntityCollection[RoleDefinition](
                self.context, RoleDefinition, ResourcePath("roleDefinitions", self.resource_path)
            ),
        )

    @odata(name="remoteAssistancePartners", navigation=True)
    @property
    def remote_assistance_partners(self) -> EntityCollection[RemoteAssistancePartner]:
        """Gets the remoteAssistancePartners property"""
        from office365.intune.devices.management.remoteassistance.partner import (
            RemoteAssistancePartner,
        )

        return self.properties.get(
            "remoteAssistancePartners",
            EntityCollection[RemoteAssistancePartner](
                self.context, RemoteAssistancePartner, ResourcePath("remoteAssistancePartners", self.resource_path)
            ),
        )

    @odata(name="troubleshootingEvents", navigation=True)
    @property
    def troubleshooting_events(self) -> EntityCollection[DeviceManagementTroubleshootingEvent]:
        """Gets the troubleshootingEvents property"""
        from office365.intune.devices.management_troubleshooting_event import (
            DeviceManagementTroubleshootingEvent,
        )

        return self.properties.get(
            "troubleshootingEvents",
            EntityCollection[DeviceManagementTroubleshootingEvent](
                self.context,
                DeviceManagementTroubleshootingEvent,
                ResourcePath("troubleshootingEvents", self.resource_path),
            ),
        )

    @odata(name="windowsInformationProtectionAppLearningSummaries", navigation=True)
    @property
    def windows_information_protection_app_learning_summaries(
        self,
    ) -> EntityCollection[WindowsInformationProtectionAppLearningSummary]:
        """Gets the windowsInformationProtectionAppLearningSummaries property"""
        from office365.intune.devices.management.windows_information_protection_app_learning_summary import (
            WindowsInformationProtectionAppLearningSummary,
        )

        return self.properties.get(
            "windowsInformationProtectionAppLearningSummaries",
            EntityCollection[WindowsInformationProtectionAppLearningSummary](
                self.context,
                WindowsInformationProtectionAppLearningSummary,
                ResourcePath("windowsInformationProtectionAppLearningSummaries", self.resource_path),
            ),
        )

    @odata(name="windowsInformationProtectionNetworkLearningSummaries", navigation=True)
    @property
    def windows_information_protection_network_learning_summaries(
        self,
    ) -> EntityCollection[WindowsInformationProtectionNetworkLearningSummary]:
        """Gets the windowsInformationProtectionNetworkLearningSummaries property"""
        from office365.intune.devices.management.windows_information_protection_network_learning_summary import (
            WindowsInformationProtectionNetworkLearningSummary,
        )

        return self.properties.get(
            "windowsInformationProtectionNetworkLearningSummaries",
            EntityCollection[WindowsInformationProtectionNetworkLearningSummary](
                self.context,
                WindowsInformationProtectionNetworkLearningSummary,
                ResourcePath("windowsInformationProtectionNetworkLearningSummaries", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagement"

    def verify_windows_enrollment_auto_discovery(self, domain_name: str) -> ClientResult[bool]:
        """verifyWindowsEnrollmentAutoDiscovery operation.

        Args:
            domain_name (str):
                domainName parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "verifyWindowsEnrollmentAutoDiscovery", {"domainName": domain_name}, return_type)
        self.context.add_query(qry)
        return return_type

    def user_experience_analytics_summarize_work_from_anywhere_devices(
        self,
    ) -> ClientResult[UserExperienceAnalyticsWorkFromAnywhereDevicesSummary]:
        """userExperienceAnalyticsSummarizeWorkFromAnywhereDevices operation."""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_devices_summary import (  # noqa: E501
            UserExperienceAnalyticsWorkFromAnywhereDevicesSummary,
        )

        return_type = ClientResult(self.context, UserExperienceAnalyticsWorkFromAnywhereDevicesSummary())
        qry = FunctionQuery(self, "userExperienceAnalyticsSummarizeWorkFromAnywhereDevices", None, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="deviceComplianceReportSummarizationDateTime", beta=True, readonly=True)
    @property
    def device_compliance_report_summarization_date_time(self) -> Optional[datetime]:
        """Gets the deviceComplianceReportSummarizationDateTime property"""
        return self.properties.get("deviceComplianceReportSummarizationDateTime", None)

    @odata(name="lastReportAggregationDateTime", beta=True, readonly=True)
    @property
    def last_report_aggregation_date_time(self) -> Optional[datetime]:
        """Gets the lastReportAggregationDateTime property"""
        return self.properties.get("lastReportAggregationDateTime", None)

    @odata(name="legacyPcManangementEnabled", beta=True, readonly=True)
    @property
    def legacy_pc_manangement_enabled(self) -> Optional[bool]:
        """Gets the legacyPcManangementEnabled property"""
        return self.properties.get("legacyPcManangementEnabled", None)

    @odata(name="maximumDepTokens", beta=True)
    @property
    def maximum_dep_tokens(self) -> Optional[int]:
        """Gets the maximumDepTokens property"""
        return self.properties.get("maximumDepTokens", None)

    @odata(name="unlicensedAdminstratorsEnabled", beta=True, readonly=True)
    @property
    def unlicensed_adminstrators_enabled(self) -> Optional[bool]:
        """Gets the unlicensedAdminstratorsEnabled property"""
        return self.properties.get("unlicensedAdminstratorsEnabled", None)

    @odata(name="accountMoveCompletionDateTime", beta=True)
    @property
    def account_move_completion_date_time(self) -> Optional[datetime]:
        """Gets the accountMoveCompletionDateTime property"""
        return self.properties.get("accountMoveCompletionDateTime", None)

    @odata(name="assignmentFilters", beta=True, navigation=True)
    @property
    def assignment_filters(self) -> EntityCollection[DeviceAndAppManagementAssignmentFilter]:
        """Gets the assignmentFilters property"""
        from office365.intune.devices.and_app_management_assignment_filter import DeviceAndAppManagementAssignmentFilter

        return self.properties.get(
            "assignmentFilters",
            EntityCollection[DeviceAndAppManagementAssignmentFilter](
                self.context,
                DeviceAndAppManagementAssignmentFilter,
                ResourcePath("assignmentFilters", self.resource_path),
            ),
        )

    @odata(name="complianceCategories", beta=True, navigation=True)
    @property
    def compliance_categories(self) -> EntityCollection[DeviceManagementConfigurationCategory]:
        """Gets the complianceCategories property"""
        from office365.intune.devices.management_configuration_category import DeviceManagementConfigurationCategory

        return self.properties.get(
            "complianceCategories",
            EntityCollection[DeviceManagementConfigurationCategory](
                self.context,
                DeviceManagementConfigurationCategory,
                ResourcePath("complianceCategories", self.resource_path),
            ),
        )

    @odata(name="compliancePolicies", beta=True, navigation=True)
    @property
    def compliance_policies(self) -> EntityCollection[DeviceManagementCompliancePolicy]:
        """Gets the compliancePolicies property"""
        from office365.intune.devices.management_compliance_policy import DeviceManagementCompliancePolicy

        return self.properties.get(
            "compliancePolicies",
            EntityCollection[DeviceManagementCompliancePolicy](
                self.context, DeviceManagementCompliancePolicy, ResourcePath("compliancePolicies", self.resource_path)
            ),
        )

    @odata(name="complianceSettings", beta=True, navigation=True)
    @property
    def compliance_settings(self) -> EntityCollection[DeviceManagementConfigurationSettingDefinition]:
        """Gets the complianceSettings property"""
        from office365.intune.devices.management_configuration_setting_definition import (
            DeviceManagementConfigurationSettingDefinition,
        )

        return self.properties.get(
            "complianceSettings",
            EntityCollection[DeviceManagementConfigurationSettingDefinition](
                self.context,
                DeviceManagementConfigurationSettingDefinition,
                ResourcePath("complianceSettings", self.resource_path),
            ),
        )

    @odata(name="configurationCategories", beta=True, navigation=True)
    @property
    def configuration_categories(self) -> EntityCollection[DeviceManagementConfigurationCategory]:
        """Gets the configurationCategories property"""
        from office365.intune.devices.management_configuration_category import DeviceManagementConfigurationCategory

        return self.properties.get(
            "configurationCategories",
            EntityCollection[DeviceManagementConfigurationCategory](
                self.context,
                DeviceManagementConfigurationCategory,
                ResourcePath("configurationCategories", self.resource_path),
            ),
        )

    @odata(name="configurationPolicies", beta=True, navigation=True)
    @property
    def configuration_policies(self) -> EntityCollection[DeviceManagementConfigurationPolicy]:
        """Gets the configurationPolicies property"""
        from office365.intune.devices.management_configuration_policy import DeviceManagementConfigurationPolicy

        return self.properties.get(
            "configurationPolicies",
            EntityCollection[DeviceManagementConfigurationPolicy](
                self.context,
                DeviceManagementConfigurationPolicy,
                ResourcePath("configurationPolicies", self.resource_path),
            ),
        )

    @odata(name="configurationPolicyTemplates", beta=True, navigation=True)
    @property
    def configuration_policy_templates(self) -> EntityCollection[DeviceManagementConfigurationPolicyTemplate]:
        """Gets the configurationPolicyTemplates property"""
        from office365.intune.devices.management_configuration_policy_template import (
            DeviceManagementConfigurationPolicyTemplate,
        )

        return self.properties.get(
            "configurationPolicyTemplates",
            EntityCollection[DeviceManagementConfigurationPolicyTemplate](
                self.context,
                DeviceManagementConfigurationPolicyTemplate,
                ResourcePath("configurationPolicyTemplates", self.resource_path),
            ),
        )

    @odata(name="configurationSettings", beta=True, navigation=True)
    @property
    def configuration_settings(self) -> EntityCollection[DeviceManagementConfigurationSettingDefinition]:
        """Gets the configurationSettings property"""
        from office365.intune.devices.management_configuration_setting_definition import (
            DeviceManagementConfigurationSettingDefinition,
        )

        return self.properties.get(
            "configurationSettings",
            EntityCollection[DeviceManagementConfigurationSettingDefinition](
                self.context,
                DeviceManagementConfigurationSettingDefinition,
                ResourcePath("configurationSettings", self.resource_path),
            ),
        )

    @odata(name="reusablePolicySettings", beta=True, navigation=True)
    @property
    def reusable_policy_settings(self) -> EntityCollection[DeviceManagementReusablePolicySetting]:
        """Gets the reusablePolicySettings property"""
        from office365.intune.devices.management_reusable_policy_setting import DeviceManagementReusablePolicySetting

        return self.properties.get(
            "reusablePolicySettings",
            EntityCollection[DeviceManagementReusablePolicySetting](
                self.context,
                DeviceManagementReusablePolicySetting,
                ResourcePath("reusablePolicySettings", self.resource_path),
            ),
        )

    @odata(name="reusableSettings", beta=True, navigation=True)
    @property
    def reusable_settings(self) -> EntityCollection[DeviceManagementConfigurationSettingDefinition]:
        """Gets the reusableSettings property"""
        from office365.intune.devices.management_configuration_setting_definition import (
            DeviceManagementConfigurationSettingDefinition,
        )

        return self.properties.get(
            "reusableSettings",
            EntityCollection[DeviceManagementConfigurationSettingDefinition](
                self.context,
                DeviceManagementConfigurationSettingDefinition,
                ResourcePath("reusableSettings", self.resource_path),
            ),
        )

    @odata(name="templateSettings", beta=True, navigation=True)
    @property
    def template_settings(self) -> EntityCollection[DeviceManagementConfigurationSettingTemplate]:
        """Gets the templateSettings property"""
        from office365.intune.devices.management_configuration_setting_template import (
            DeviceManagementConfigurationSettingTemplate,
        )

        return self.properties.get(
            "templateSettings",
            EntityCollection[DeviceManagementConfigurationSettingTemplate](
                self.context,
                DeviceManagementConfigurationSettingTemplate,
                ResourcePath("templateSettings", self.resource_path),
            ),
        )

    @odata(name="comanagedDevices", beta=True, navigation=True)
    @property
    def comanaged_devices(self) -> EntityCollection[ManagedDevice]:
        """Gets the comanagedDevices property"""
        from office365.intune.devices.management.managed.managed import ManagedDevice

        return self.properties.get(
            "comanagedDevices",
            EntityCollection[ManagedDevice](
                self.context, ManagedDevice, ResourcePath("comanagedDevices", self.resource_path)
            ),
        )

    @odata(name="userExperienceAnalyticsDeviceMetricHistory", beta=True, navigation=True)
    @property
    def user_experience_analytics_device_metric_history(self) -> EntityCollection[UserExperienceAnalyticsMetricHistory]:
        """Gets the userExperienceAnalyticsDeviceMetricHistory property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_metric_history import (  # noqa: E501
            UserExperienceAnalyticsMetricHistory,
        )

        return self.properties.get(
            "userExperienceAnalyticsDeviceMetricHistory",
            EntityCollection[UserExperienceAnalyticsMetricHistory](
                self.context,
                UserExperienceAnalyticsMetricHistory,
                ResourcePath("userExperienceAnalyticsDeviceMetricHistory", self.resource_path),
            ),
        )

    @odata(name="windowsAutopilotDeploymentProfiles", beta=True, navigation=True)
    @property
    def windows_autopilot_deployment_profiles(self) -> EntityCollection[WindowsAutopilotDeploymentProfile]:
        """Gets the windowsAutopilotDeploymentProfiles property"""
        from office365.intune.devices.management.windows_autopilot_deployment_profile import (
            WindowsAutopilotDeploymentProfile,
        )

        return self.properties.get(
            "windowsAutopilotDeploymentProfiles",
            EntityCollection[WindowsAutopilotDeploymentProfile](
                self.context,
                WindowsAutopilotDeploymentProfile,
                ResourcePath("windowsAutopilotDeploymentProfiles", self.resource_path),
            ),
        )

    @odata(name="groupPolicyMigrationReports", beta=True, navigation=True)
    @property
    def group_policy_migration_reports(self) -> EntityCollection[GroupPolicyMigrationReport]:
        """Gets the groupPolicyMigrationReports property"""
        from office365.common.group_policy_migration_report import GroupPolicyMigrationReport

        return self.properties.get(
            "groupPolicyMigrationReports",
            EntityCollection[GroupPolicyMigrationReport](
                self.context, GroupPolicyMigrationReport, ResourcePath("groupPolicyMigrationReports", self.resource_path)
            ),
        )

    @odata(name="groupPolicyObjectFiles", beta=True, navigation=True)
    @property
    def group_policy_object_files(self) -> EntityCollection[GroupPolicyObjectFile]:
        """Gets the groupPolicyObjectFiles property"""
        from office365.common.group_policy_object_file import GroupPolicyObjectFile

        return self.properties.get(
            "groupPolicyObjectFiles",
            EntityCollection[GroupPolicyObjectFile](
                self.context, GroupPolicyObjectFile, ResourcePath("groupPolicyObjectFiles", self.resource_path)
            ),
        )

    @odata(name="groupPolicyCategories", beta=True, navigation=True)
    @property
    def group_policy_categories(self) -> EntityCollection[GroupPolicyCategory]:
        """Gets the groupPolicyCategories property"""
        from office365.common.group_policy_category import GroupPolicyCategory

        return self.properties.get(
            "groupPolicyCategories",
            EntityCollection[GroupPolicyCategory](
                self.context, GroupPolicyCategory, ResourcePath("groupPolicyCategories", self.resource_path)
            ),
        )

    @odata(name="groupPolicyConfigurations", beta=True, navigation=True)
    @property
    def group_policy_configurations(self) -> EntityCollection[GroupPolicyConfiguration]:
        """Gets the groupPolicyConfigurations property"""
        from office365.common.group_policy_configuration import GroupPolicyConfiguration

        return self.properties.get(
            "groupPolicyConfigurations",
            EntityCollection[GroupPolicyConfiguration](
                self.context, GroupPolicyConfiguration, ResourcePath("groupPolicyConfigurations", self.resource_path)
            ),
        )

    @odata(name="groupPolicyDefinitionFiles", beta=True, navigation=True)
    @property
    def group_policy_definition_files(self) -> EntityCollection[GroupPolicyDefinitionFile]:
        """Gets the groupPolicyDefinitionFiles property"""
        from office365.common.group_policy_definition_file import GroupPolicyDefinitionFile

        return self.properties.get(
            "groupPolicyDefinitionFiles",
            EntityCollection[GroupPolicyDefinitionFile](
                self.context, GroupPolicyDefinitionFile, ResourcePath("groupPolicyDefinitionFiles", self.resource_path)
            ),
        )

    @odata(name="groupPolicyDefinitions", beta=True, navigation=True)
    @property
    def group_policy_definitions(self) -> EntityCollection[GroupPolicyDefinition]:
        """Gets the groupPolicyDefinitions property"""
        from office365.common.group_policy_definition import GroupPolicyDefinition

        return self.properties.get(
            "groupPolicyDefinitions",
            EntityCollection[GroupPolicyDefinition](
                self.context, GroupPolicyDefinition, ResourcePath("groupPolicyDefinitions", self.resource_path)
            ),
        )

    @odata(name="groupPolicyUploadedDefinitionFiles", beta=True, navigation=True)
    @property
    def group_policy_uploaded_definition_files(self) -> EntityCollection[GroupPolicyUploadedDefinitionFile]:
        """Gets the groupPolicyUploadedDefinitionFiles property"""
        from office365.common.group_policy_uploaded_definition_file import GroupPolicyUploadedDefinitionFile

        return self.properties.get(
            "groupPolicyUploadedDefinitionFiles",
            EntityCollection[GroupPolicyUploadedDefinitionFile](
                self.context,
                GroupPolicyUploadedDefinitionFile,
                ResourcePath("groupPolicyUploadedDefinitionFiles", self.resource_path),
            ),
        )

    @odata(name="enableAndroidDeviceAdministratorEnrollment", beta=True, selectable=False)
    def enable_android_device_administrator_enrollment(self) -> Self:
        """enableAndroidDeviceAdministratorEnrollment operation."""
        qry = ServiceOperationQuery(self, "enableAndroidDeviceAdministratorEnrollment", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="enableEndpointPrivilegeManagement", beta=True, selectable=False)
    def enable_endpoint_privilege_management(self) -> Self:
        """enableEndpointPrivilegeManagement operation."""
        qry = ServiceOperationQuery(self, "enableEndpointPrivilegeManagement", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="enableLegacyPcManagement", beta=True, selectable=False)
    def enable_legacy_pc_management(self) -> Self:
        """enableLegacyPcManagement operation."""
        qry = ServiceOperationQuery(self, "enableLegacyPcManagement", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="enableUnlicensedAdminstrators", beta=True, selectable=False)
    def enable_unlicensed_adminstrators(self) -> Self:
        """enableUnlicensedAdminstrators operation."""
        qry = ServiceOperationQuery(self, "enableUnlicensedAdminstrators", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="sendCustomNotificationToCompanyPortal", beta=True, selectable=False)
    def send_custom_notification_to_company_portal(
        self, notification_title: str, notification_body: str, groups_to_notify: list[str]
    ) -> Self:
        """sendCustomNotificationToCompanyPortal operation.

        Args:
            notification_title (str):
                notificationTitle parameter
            notification_body (str):
                notificationBody parameter
            groups_to_notify (list[str]):
                groupsToNotify parameter
        """
        qry = ServiceOperationQuery(
            self,
            "sendCustomNotificationToCompanyPortal",
            None,
            {
                "notificationTitle": notification_title,
                "notificationBody": notification_body,
                "groupsToNotify": StringCollection(groups_to_notify),
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    @odata(name="scopedForResource", beta=True, selectable=False)
    def scoped_for_resource(self, resource: str) -> ClientResult[bool]:
        """scopedForResource operation.

        Args:
            resource (str):
                resource parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "scopedForResource", {"resource": resource}, return_type)
        self.context.add_query(qry)
        return return_type
