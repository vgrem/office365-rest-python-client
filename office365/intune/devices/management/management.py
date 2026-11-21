from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from typing_extensions import Self

from office365.directory.rolemanagement.roles.permission import RolePermission
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.audit.event_collection import AuditEventCollection
from office365.intune.brand import IntuneBrand
from office365.intune.devices.category_collection import DeviceCategoryCollection
from office365.intune.devices.enrollment.configuration import (
    DeviceEnrollmentConfiguration,
)
from office365.intune.devices.management.managed.collection import (
    ManagedDeviceCollection,
)
from office365.intune.devices.management.protection_overview import DeviceProtectionOverview
from office365.intune.devices.management.reports.reports import DeviceManagementReports
from office365.intune.devices.management.settings import DeviceManagementSettings
from office365.intune.devices.management.subscriptionstate import DeviceManagementSubscriptionState
from office365.intune.devices.management.terms_and_conditions import TermsAndConditions
from office365.intune.devices.management.userexperienceanalytics.settings import UserExperienceAnalyticsSettings
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_severity_overview import (  # noqa: E501
    UserExperienceAnalyticsAnomalySeverityOverview,
)
from office365.intune.devices.management.virtualendpoint.virtual_endpoint import (
    VirtualEndpoint,
)
from office365.intune.devices.management.windowsmalware.overview import WindowsMalwareOverview
from office365.permissions import require_permission, requires_license
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.common.role_definition import RoleDefinition
    from office365.intune.audit.remote_action_audit import RemoteActionAudit
    from office365.intune.devices.compliance.management_partner import (
        ComplianceManagementPartner,
    )
    from office365.intune.devices.compliance.policy import DeviceCompliancePolicy
    from office365.intune.devices.compliance.policy_device_state_summary import (
        DeviceCompliancePolicyDeviceStateSummary,
    )
    from office365.intune.devices.compliance.policy_setting_state_summary import (
        DeviceCompliancePolicySettingStateSummary,
    )
    from office365.intune.devices.compliance.restricted_apps_violation import RestrictedAppsViolation
    from office365.intune.devices.compliance.script import DeviceComplianceScript
    from office365.intune.devices.configurations.configuration import (
        DeviceConfiguration,
    )
    from office365.intune.devices.configurations.conflict_summary import DeviceConfigurationConflictSummary
    from office365.intune.devices.configurations.state_summary import (
        DeviceConfigurationDeviceStateSummary,
    )
    from office365.intune.devices.configurations.user_state_summary import DeviceConfigurationUserStateSummary
    from office365.intune.devices.custom_attribute_shell_script import DeviceCustomAttributeShellScript
    from office365.intune.devices.enrollment.android_device_owner_enrollment_profile import (
        AndroidDeviceOwnerEnrollmentProfile,
    )
    from office365.intune.devices.enrollment.android_for_work_enrollment_profile import AndroidForWorkEnrollmentProfile
    from office365.intune.devices.enrollment.android_for_work_settings import AndroidForWorkSettings
    from office365.intune.devices.enrollment.apple_user_initiated_enrollment_profile import (
        AppleUserInitiatedEnrollmentProfile,
    )
    from office365.intune.devices.enrollment.dep_onboarding_setting import DepOnboardingSetting
    from office365.intune.devices.enrollment.imported_device_identity import ImportedDeviceIdentity
    from office365.intune.devices.health_script import DeviceHealthScript
    from office365.intune.devices.management.apple_push_notification_certificate import (
        ApplePushNotificationCertificate,
    )
    from office365.intune.devices.management.assignment_filter import DeviceAndAppManagementAssignmentFilter
    from office365.intune.devices.management.autopilot_event import DeviceManagementAutopilotEvent
    from office365.intune.devices.management.cart_to_class_association import CartToClassAssociation
    from office365.intune.devices.management.certificate_connector_details import CertificateConnectorDetails
    from office365.intune.devices.management.chrome_os_onboarding_settings import ChromeOSOnboardingSettings
    from office365.intune.devices.management.comanagement_eligible_device import ComanagementEligibleDevice
    from office365.intune.devices.management.compliance_policy import DeviceManagementCompliancePolicy
    from office365.intune.devices.management.config_manager_collection import ConfigManagerCollection
    from office365.intune.devices.management.configuration.category import DeviceManagementConfigurationCategory
    from office365.intune.devices.management.configuration.policy import DeviceManagementConfigurationPolicy
    from office365.intune.devices.management.configuration.policy_template import (
        DeviceManagementConfigurationPolicyTemplate,
    )
    from office365.intune.devices.management.configuration.settings.definition import (
        DeviceManagementConfigurationSettingDefinition,
    )
    from office365.intune.devices.management.configuration.settings.template import (
        DeviceManagementConfigurationSettingTemplate,
    )
    from office365.intune.devices.management.data_sharing_consent import DataSharingConsent
    from office365.intune.devices.management.detected_app import DetectedApp
    from office365.intune.devices.management.domain_join_connector import DeviceManagementDomainJoinConnector
    from office365.intune.devices.management.exchangeconnectors.exchange_connector import (
        DeviceManagementExchangeConnector,
    )
    from office365.intune.devices.management.grouppolicies.category import GroupPolicyCategory
    from office365.intune.devices.management.grouppolicies.configuration import GroupPolicyConfiguration
    from office365.intune.devices.management.grouppolicies.definition import GroupPolicyDefinition
    from office365.intune.devices.management.grouppolicies.definition_file import GroupPolicyDefinitionFile
    from office365.intune.devices.management.grouppolicies.migration_report import GroupPolicyMigrationReport
    from office365.intune.devices.management.grouppolicies.object_file import GroupPolicyObjectFile
    from office365.intune.devices.management.grouppolicies.uploaded_definition_file import (
        GroupPolicyUploadedDefinitionFile,
    )
    from office365.intune.devices.management.hardware_password_detail import HardwarePasswordDetail
    from office365.intune.devices.management.hardware_password_info import HardwarePasswordInfo
    from office365.intune.devices.management.imported_windows_autopilot_device_identity import (
        ImportedWindowsAutopilotDeviceIdentity,
    )
    from office365.intune.devices.management.intents.intent import DeviceManagementIntent
    from office365.intune.devices.management.managed.all_device_certificate_state import ManagedAllDeviceCertificateState
    from office365.intune.devices.management.managed.android.store_account_enterprise_settings import (
        AndroidManagedStoreAccountEnterpriseSettings,
    )
    from office365.intune.devices.management.managed.android.store_app_configuration_schema import (
        AndroidManagedStoreAppConfigurationSchema,
    )
    from office365.intune.devices.management.managed.device import ManagedDevice
    from office365.intune.devices.management.managed.encryption_state import ManagedDeviceEncryptionState
    from office365.intune.devices.management.managed.ios.update_device_status import IosUpdateDeviceStatus
    from office365.intune.devices.management.managed.overview import ManagedDeviceOverview
    from office365.intune.devices.management.managed.windows.autopilot_deployment_profile import (
        WindowsAutopilotDeploymentProfile,
    )
    from office365.intune.devices.management.managed.windows.autopilot_device_identity import (
        WindowsAutopilotDeviceIdentity,
    )
    from office365.intune.devices.management.managed.windows.autopilot_settings import WindowsAutopilotSettings
    from office365.intune.devices.management.microsoft_tunnel_configuration import MicrosoftTunnelConfiguration
    from office365.intune.devices.management.microsoft_tunnel_health_threshold import MicrosoftTunnelHealthThreshold
    from office365.intune.devices.management.microsoft_tunnel_site import MicrosoftTunnelSite
    from office365.intune.devices.management.mobile_threat_defense_connector import (
        MobileThreatDefenseConnector,
    )
    from office365.intune.devices.management.mobileapps.troubleshooting_event import (
        MobileAppTroubleshootingEvent,
    )
    from office365.intune.devices.management.notification_message_template import (
        NotificationMessageTemplate,
    )
    from office365.intune.devices.management.on_premises_conditional_access_settings import (
        OnPremisesConditionalAccessSettings,
    )
    from office365.intune.devices.management.partner import DeviceManagementPartner
    from office365.intune.devices.management.remoteassistance.partner import (
        RemoteAssistancePartner,
    )
    from office365.intune.devices.management.resource_operation import ResourceOperation
    from office365.intune.devices.management.reusable_policy_setting import DeviceManagementReusablePolicySetting
    from office365.intune.devices.management.role_assignment import (
        DeviceAndAppManagementRoleAssignment,
    )
    from office365.intune.devices.management.role_scope_tag import RoleScopeTag
    from office365.intune.devices.management.script import DeviceManagementScript
    from office365.intune.devices.management.software_update_status_summary import (
        SoftwareUpdateStatusSummary,
    )
    from office365.intune.devices.management.troubleshooting_event import (
        DeviceManagementTroubleshootingEvent,
    )
    from office365.intune.devices.management.user_pfx_certificate import UserPFXCertificate
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly import (
        UserExperienceAnalyticsAnomaly,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_correlation_group_overview import (  # noqa: E501
        UserExperienceAnalyticsAnomalyCorrelationGroupOverview,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_device import (
        UserExperienceAnalyticsAnomalyDevice,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_app_performance_by_app_version import (  # noqa: E501
        UserExperienceAnalyticsAppHealthAppPerformanceByAppVersion,
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
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_app_impact import (  # noqa: E501
        UserExperienceAnalyticsBatteryHealthAppImpact,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_capacity_details import (  # noqa: E501
        UserExperienceAnalyticsBatteryHealthCapacityDetails,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_device_app_impact import (  # noqa: E501
        UserExperienceAnalyticsBatteryHealthDeviceAppImpact,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_device_performance import (  # noqa: E501
        UserExperienceAnalyticsBatteryHealthDevicePerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_device_runtime_history import (  # noqa: E501
        UserExperienceAnalyticsBatteryHealthDeviceRuntimeHistory,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_model_performance import (  # noqa: E501
        UserExperienceAnalyticsBatteryHealthModelPerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_os_performance import (  # noqa: E501
        UserExperienceAnalyticsBatteryHealthOsPerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_runtime_details import (  # noqa: E501
        UserExperienceAnalyticsBatteryHealthRuntimeDetails,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_category import (
        UserExperienceAnalyticsCategory,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_performance import (  # noqa: E501
        UserExperienceAnalyticsDevicePerformance,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_scope import (
        UserExperienceAnalyticsDeviceScope,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_scope_summary import (  # noqa: E501
        UserExperienceAnalyticsDeviceScopeSummary,
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
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_timeline_event import (  # noqa: E501
        UserExperienceAnalyticsDeviceTimelineEvent,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_without_cloud_identity import (  # noqa: E501
        UserExperienceAnalyticsDeviceWithoutCloudIdentity,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_impacting_process import (
        UserExperienceAnalyticsImpactingProcess,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_metric_history import (
        UserExperienceAnalyticsMetricHistory,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_model_scores import (
        UserExperienceAnalyticsModelScores,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_not_autopilot_ready_device import (  # noqa: E501
        UserExperienceAnalyticsNotAutopilotReadyDevice,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_overview import (
        UserExperienceAnalyticsOverview,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_remote_connection import (
        UserExperienceAnalyticsRemoteConnection,
    )
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_resource_performance import (  # noqa: E501
        UserExperienceAnalyticsResourcePerformance,
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
    from office365.intune.devices.management.virtualendpoint.cloudpcs.cloud_pc_connectivity_issue import (
        CloudPCConnectivityIssue,
    )
    from office365.intune.devices.management.windows_information_protection_app_learning_summary import (
        WindowsInformationProtectionAppLearningSummary,
    )
    from office365.intune.devices.management.windows_information_protection_network_learning_summary import (
        WindowsInformationProtectionNetworkLearningSummary,
    )
    from office365.intune.devices.management.windowsmalware.windows_malware_information import WindowsMalwareInformation
    from office365.intune.devices.shell_script import DeviceShellScript
    from office365.intune.windows_driver_update_profile import WindowsDriverUpdateProfile
    from office365.intune.windows_feature_update_profile import WindowsFeatureUpdateProfile
    from office365.intune.windows_quality_update_profile import WindowsQualityUpdateProfile


@requires_license("INTUNE_A")
class DeviceManagement(Entity):
    """
    The deviceManagement resource represents a tenant's collection device identities that have been pre-staged in
    Intune, and the enrollment profiles that may be assigned to device identities that support pre-enrollment
    configuration.
    """

    @verb(role="action", effect="read")
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
    def device_categories(self) -> DeviceCategoryCollection:
        """"""
        return self.properties.get(
            "deviceCategories",
            DeviceCategoryCollection(
                self.context,
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
        from office365.intune.devices.compliance.policy_device_state_summary import (
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
        from office365.intune.devices.compliance.policy_setting_state_summary import (
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
        from office365.intune.devices.configurations.state_summary import (
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
        from office365.intune.devices.management.managed.ios.update_device_status import IosUpdateDeviceStatus

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
        from office365.intune.devices.management.partner import DeviceManagementPartner

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
        from office365.intune.devices.management.exchangeconnectors.exchange_connector import (
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
        from office365.intune.devices.management.managed.overview import ManagedDeviceOverview

        return self.properties.get(
            "managedDeviceOverview",
            ManagedDeviceOverview(self.context, ResourcePath("managedDeviceOverview", self.resource_path)),
        )

    @odata(name="mobileAppTroubleshootingEvents", navigation=True)
    @property
    def mobile_app_troubleshooting_events(self) -> EntityCollection[MobileAppTroubleshootingEvent]:
        """Gets the mobileAppTroubleshootingEvents property"""
        from office365.intune.devices.management.mobileapps.troubleshooting_event import (
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
        from office365.intune.devices.management.managed.windows.autopilot_device_identity import (
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
        from office365.intune.devices.management.role_assignment import (
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
        from office365.intune.devices.management.troubleshooting_event import (
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

    @verb(role="action", effect="read")
    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All", "DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All", "DeviceManagementConfiguration.ReadWrite.All"],
    )
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

    @verb(role="action", effect="read")
    @require_permission(
        delegated=["DeviceManagementManagedDevices.Read.All", "DeviceManagementManagedDevices.ReadWrite.All"],
        application=["DeviceManagementManagedDevices.Read.All", "DeviceManagementManagedDevices.ReadWrite.All"],
    )
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
        from office365.intune.devices.management.assignment_filter import DeviceAndAppManagementAssignmentFilter

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
        from office365.intune.devices.management.configuration.category import DeviceManagementConfigurationCategory

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
        from office365.intune.devices.management.compliance_policy import DeviceManagementCompliancePolicy

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
        from office365.intune.devices.management.configuration.settings.definition import (
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
        from office365.intune.devices.management.configuration.category import DeviceManagementConfigurationCategory

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
        from office365.intune.devices.management.configuration.policy import DeviceManagementConfigurationPolicy

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
        from office365.intune.devices.management.configuration.policy_template import (
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
        from office365.intune.devices.management.configuration.settings.definition import (
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
        from office365.intune.devices.management.reusable_policy_setting import DeviceManagementReusablePolicySetting

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
        from office365.intune.devices.management.configuration.settings.definition import (
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
        from office365.intune.devices.management.configuration.settings.template import (
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
        from office365.intune.devices.management.managed.device import ManagedDevice

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
        from office365.intune.devices.management.managed.windows.autopilot_deployment_profile import (
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
        from office365.intune.devices.management.grouppolicies.migration_report import GroupPolicyMigrationReport

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
        from office365.intune.devices.management.grouppolicies.object_file import GroupPolicyObjectFile

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
        from office365.intune.devices.management.grouppolicies.category import GroupPolicyCategory

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
        from office365.intune.devices.management.grouppolicies.configuration import GroupPolicyConfiguration

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
        from office365.intune.devices.management.grouppolicies.definition_file import GroupPolicyDefinitionFile

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
        from office365.intune.devices.management.grouppolicies.definition import GroupPolicyDefinition

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
        from office365.intune.devices.management.grouppolicies.uploaded_definition_file import (
            GroupPolicyUploadedDefinitionFile,
        )

        return self.properties.get(
            "groupPolicyUploadedDefinitionFiles",
            EntityCollection[GroupPolicyUploadedDefinitionFile](
                self.context,
                GroupPolicyUploadedDefinitionFile,
                ResourcePath("groupPolicyUploadedDefinitionFiles", self.resource_path),
            ),
        )

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All"],
    )
    @odata(name="enableAndroidDeviceAdministratorEnrollment", beta=True, selectable=False)
    def enable_android_device_administrator_enrollment(self) -> Self:
        """enableAndroidDeviceAdministratorEnrollment operation."""
        qry = ServiceOperationQuery(self, "enableAndroidDeviceAdministratorEnrollment", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All"],
    )
    @odata(name="enableEndpointPrivilegeManagement", beta=True, selectable=False)
    def enable_endpoint_privilege_management(self) -> Self:
        """enableEndpointPrivilegeManagement operation."""
        qry = ServiceOperationQuery(self, "enableEndpointPrivilegeManagement", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All"],
    )
    @odata(name="enableLegacyPcManagement", beta=True, selectable=False)
    def enable_legacy_pc_management(self) -> Self:
        """enableLegacyPcManagement operation."""
        qry = ServiceOperationQuery(self, "enableLegacyPcManagement", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All"],
    )
    @odata(name="enableUnlicensedAdminstrators", beta=True, selectable=False)
    def enable_unlicensed_adminstrators(self) -> Self:
        """enableUnlicensedAdminstrators operation."""
        qry = ServiceOperationQuery(self, "enableUnlicensedAdminstrators", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All"],
    )
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

    @verb(role="action", effect="read")
    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementRBAC.Read.All",
            "DeviceManagementRBAC.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementRBAC.Read.All",
            "DeviceManagementRBAC.ReadWrite.All",
        ],
    )
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

    @odata(name="androidManagedStoreAppConfigurationSchemas", beta=True, navigation=True)
    @property
    def android_managed_store_app_configuration_schemas(
        self,
    ) -> EntityCollection[AndroidManagedStoreAppConfigurationSchema]:
        """Gets the androidManagedStoreAppConfigurationSchemas property"""
        from office365.intune.devices.management.managed.android.store_app_configuration_schema import (
            AndroidManagedStoreAppConfigurationSchema,
        )

        return self.properties.get(
            "androidManagedStoreAppConfigurationSchemas",
            EntityCollection[AndroidManagedStoreAppConfigurationSchema](
                self.context,
                AndroidManagedStoreAppConfigurationSchema,
                ResourcePath("androidManagedStoreAppConfigurationSchemas", self.resource_path),
            ),
        )

    @odata(name="microsoftTunnelConfigurations", beta=True, navigation=True)
    @property
    def microsoft_tunnel_configurations(self) -> EntityCollection[MicrosoftTunnelConfiguration]:
        """Gets the microsoftTunnelConfigurations property"""
        from office365.intune.devices.management.microsoft_tunnel_configuration import MicrosoftTunnelConfiguration

        return self.properties.get(
            "microsoftTunnelConfigurations",
            EntityCollection[MicrosoftTunnelConfiguration](
                self.context,
                MicrosoftTunnelConfiguration,
                ResourcePath("microsoftTunnelConfigurations", self.resource_path),
            ),
        )

    @odata(name="microsoftTunnelHealthThresholds", beta=True, navigation=True)
    @property
    def microsoft_tunnel_health_thresholds(self) -> EntityCollection[MicrosoftTunnelHealthThreshold]:
        """Gets the microsoftTunnelHealthThresholds property"""
        from office365.intune.devices.management.microsoft_tunnel_health_threshold import MicrosoftTunnelHealthThreshold

        return self.properties.get(
            "microsoftTunnelHealthThresholds",
            EntityCollection[MicrosoftTunnelHealthThreshold](
                self.context,
                MicrosoftTunnelHealthThreshold,
                ResourcePath("microsoftTunnelHealthThresholds", self.resource_path),
            ),
        )

    @odata(name="windowsFeatureUpdateProfiles", beta=True, navigation=True)
    @property
    def windows_feature_update_profiles(self) -> EntityCollection[WindowsFeatureUpdateProfile]:
        """Gets the windowsFeatureUpdateProfiles property"""
        from office365.intune.windows_feature_update_profile import WindowsFeatureUpdateProfile

        return self.properties.get(
            "windowsFeatureUpdateProfiles",
            EntityCollection[WindowsFeatureUpdateProfile](
                self.context,
                WindowsFeatureUpdateProfile,
                ResourcePath("windowsFeatureUpdateProfiles", self.resource_path),
            ),
        )

    @odata(name="windowsQualityUpdateProfiles", beta=True, navigation=True)
    @property
    def windows_quality_update_profiles(self) -> EntityCollection[WindowsQualityUpdateProfile]:
        """Gets the windowsQualityUpdateProfiles property"""
        from office365.intune.windows_quality_update_profile import WindowsQualityUpdateProfile

        return self.properties.get(
            "windowsQualityUpdateProfiles",
            EntityCollection[WindowsQualityUpdateProfile](
                self.context,
                WindowsQualityUpdateProfile,
                ResourcePath("windowsQualityUpdateProfiles", self.resource_path),
            ),
        )

    @odata(name="androidManagedStoreAccountEnterpriseSettings", beta=True, navigation=True)
    @property
    def android_managed_store_account_enterprise_settings(self) -> AndroidManagedStoreAccountEnterpriseSettings:
        """Gets the androidManagedStoreAccountEnterpriseSettings property"""
        from office365.intune.devices.management.managed.android.store_account_enterprise_settings import (
            AndroidManagedStoreAccountEnterpriseSettings,
        )

        return self.properties.get(
            "androidManagedStoreAccountEnterpriseSettings",
            AndroidManagedStoreAccountEnterpriseSettings(
                self.context, ResourcePath("androidManagedStoreAccountEnterpriseSettings", self.resource_path)
            ),
        )

    @odata(name="microsoftTunnelSites", beta=True, navigation=True)
    @property
    def microsoft_tunnel_sites(self) -> EntityCollection[MicrosoftTunnelSite]:
        """Gets the microsoftTunnelSites property"""
        from office365.intune.devices.management.microsoft_tunnel_site import MicrosoftTunnelSite

        return self.properties.get(
            "microsoftTunnelSites",
            EntityCollection[MicrosoftTunnelSite](
                self.context, MicrosoftTunnelSite, ResourcePath("microsoftTunnelSites", self.resource_path)
            ),
        )

    @odata(name="deviceComplianceScripts", beta=True, navigation=True)
    @property
    def device_compliance_scripts(self) -> EntityCollection[DeviceComplianceScript]:
        """Gets the deviceComplianceScripts property"""
        from office365.intune.devices.compliance.script import DeviceComplianceScript

        return self.properties.get(
            "deviceComplianceScripts",
            EntityCollection[DeviceComplianceScript](
                self.context, DeviceComplianceScript, ResourcePath("deviceComplianceScripts", self.resource_path)
            ),
        )

    @odata(name="deviceManagementScripts", beta=True, navigation=True)
    @property
    def device_management_scripts(self) -> EntityCollection[DeviceManagementScript]:
        """Gets the deviceManagementScripts property"""
        from office365.intune.devices.management.script import DeviceManagementScript

        return self.properties.get(
            "deviceManagementScripts",
            EntityCollection[DeviceManagementScript](
                self.context, DeviceManagementScript, ResourcePath("deviceManagementScripts", self.resource_path)
            ),
        )

    @odata(name="deviceShellScripts", beta=True, navigation=True)
    @property
    def device_shell_scripts(self) -> EntityCollection[DeviceShellScript]:
        """Gets the deviceShellScripts property"""
        from office365.intune.devices.shell_script import DeviceShellScript

        return self.properties.get(
            "deviceShellScripts",
            EntityCollection[DeviceShellScript](
                self.context, DeviceShellScript, ResourcePath("deviceShellScripts", self.resource_path)
            ),
        )

    @odata(name="deviceCustomAttributeShellScripts", beta=True, navigation=True)
    @property
    def device_custom_attribute_shell_scripts(self) -> EntityCollection[DeviceCustomAttributeShellScript]:
        """Gets the deviceCustomAttributeShellScripts property"""
        from office365.intune.devices.custom_attribute_shell_script import DeviceCustomAttributeShellScript

        return self.properties.get(
            "deviceCustomAttributeShellScripts",
            EntityCollection[DeviceCustomAttributeShellScript](
                self.context,
                DeviceCustomAttributeShellScript,
                ResourcePath("deviceCustomAttributeShellScripts", self.resource_path),
            ),
        )

    @odata(name="windowsDriverUpdateProfiles", beta=True, navigation=True)
    @property
    def windows_driver_update_profiles(self) -> EntityCollection[WindowsDriverUpdateProfile]:
        """Gets the windowsDriverUpdateProfiles property"""
        from office365.intune.windows_driver_update_profile import WindowsDriverUpdateProfile

        return self.properties.get(
            "windowsDriverUpdateProfiles",
            EntityCollection[WindowsDriverUpdateProfile](
                self.context, WindowsDriverUpdateProfile, ResourcePath("windowsDriverUpdateProfiles", self.resource_path)
            ),
        )

    @odata(name="deviceHealthScripts", beta=True, navigation=True)
    @property
    def device_health_scripts(self) -> EntityCollection[DeviceHealthScript]:
        """Gets the deviceHealthScripts property"""
        from office365.intune.devices.health_script import DeviceHealthScript

        return self.properties.get(
            "deviceHealthScripts",
            EntityCollection[DeviceHealthScript](
                self.context, DeviceHealthScript, ResourcePath("deviceHealthScripts", self.resource_path)
            ),
        )

    @odata(name="intents", beta=True, navigation=True)
    @property
    def intents(self) -> EntityCollection[DeviceManagementIntent]:
        """Gets the intents property"""
        from office365.intune.devices.management.intents.intent import DeviceManagementIntent

        return self.properties.get(
            "intents",
            EntityCollection[DeviceManagementIntent](
                self.context, DeviceManagementIntent, ResourcePath("intents", self.resource_path)
            ),
        )

    @odata(name="chromeOSOnboardingSettings", beta=True, navigation=True)
    @property
    def chrome_os_onboarding_settings(self) -> EntityCollection[ChromeOSOnboardingSettings]:
        """Gets the chromeOSOnboardingSettings property"""
        from office365.intune.devices.management.chrome_os_onboarding_settings import ChromeOSOnboardingSettings

        return self.properties.get(
            "chromeOSOnboardingSettings",
            EntityCollection[ChromeOSOnboardingSettings](
                self.context, ChromeOSOnboardingSettings, ResourcePath("chromeOSOnboardingSettings", self.resource_path)
            ),
        )

    @odata(name="cartToClassAssociations", beta=True, navigation=True)
    @property
    def cart_to_class_associations(self) -> EntityCollection[CartToClassAssociation]:
        """Gets the cartToClassAssociations property"""
        from office365.intune.devices.management.cart_to_class_association import CartToClassAssociation

        return self.properties.get(
            "cartToClassAssociations",
            EntityCollection[CartToClassAssociation](
                self.context, CartToClassAssociation, ResourcePath("cartToClassAssociations", self.resource_path)
            ),
        )

    @odata(name="hardwarePasswordDetails", beta=True, navigation=True)
    @property
    def hardware_password_details(self) -> EntityCollection[HardwarePasswordDetail]:
        """Gets the hardwarePasswordDetails property"""
        from office365.intune.devices.management.hardware_password_detail import HardwarePasswordDetail

        return self.properties.get(
            "hardwarePasswordDetails",
            EntityCollection[HardwarePasswordDetail](
                self.context, HardwarePasswordDetail, ResourcePath("hardwarePasswordDetails", self.resource_path)
            ),
        )

    @odata(name="hardwarePasswordInfo", beta=True, navigation=True)
    @property
    def hardware_password_info(self) -> EntityCollection[HardwarePasswordInfo]:
        """Gets the hardwarePasswordInfo property"""
        from office365.intune.devices.management.hardware_password_info import HardwarePasswordInfo

        return self.properties.get(
            "hardwarePasswordInfo",
            EntityCollection[HardwarePasswordInfo](
                self.context, HardwarePasswordInfo, ResourcePath("hardwarePasswordInfo", self.resource_path)
            ),
        )

    @odata(name="cloudPCConnectivityIssues", beta=True, navigation=True)
    @property
    def cloud_pc_connectivity_issues(self) -> EntityCollection[CloudPCConnectivityIssue]:
        """Gets the cloudPCConnectivityIssues property"""
        from office365.intune.devices.management.virtualendpoint.cloudpcs.cloud_pc_connectivity_issue import (
            CloudPCConnectivityIssue,
        )

        return self.properties.get(
            "cloudPCConnectivityIssues",
            EntityCollection[CloudPCConnectivityIssue](
                self.context, CloudPCConnectivityIssue, ResourcePath("cloudPCConnectivityIssues", self.resource_path)
            ),
        )

    @odata(name="dataSharingConsents", beta=True, navigation=True)
    @property
    def data_sharing_consents(self) -> EntityCollection[DataSharingConsent]:
        """Gets the dataSharingConsents property"""
        from office365.intune.devices.management.data_sharing_consent import DataSharingConsent

        return self.properties.get(
            "dataSharingConsents",
            EntityCollection[DataSharingConsent](
                self.context, DataSharingConsent, ResourcePath("dataSharingConsents", self.resource_path)
            ),
        )

    @odata(name="configManagerCollections", beta=True, navigation=True)
    @property
    def config_manager_collections(self) -> EntityCollection[ConfigManagerCollection]:
        """Gets the configManagerCollections property"""
        from office365.intune.devices.management.config_manager_collection import ConfigManagerCollection

        return self.properties.get(
            "configManagerCollections",
            EntityCollection[ConfigManagerCollection](
                self.context, ConfigManagerCollection, ResourcePath("configManagerCollections", self.resource_path)
            ),
        )

    @odata(name="certificateConnectorDetails", beta=True, navigation=True)
    @property
    def certificate_connector_details(self) -> EntityCollection[CertificateConnectorDetails]:
        """Gets the certificateConnectorDetails property"""
        from office365.intune.devices.management.certificate_connector_details import CertificateConnectorDetails

        return self.properties.get(
            "certificateConnectorDetails",
            EntityCollection[CertificateConnectorDetails](
                self.context,
                CertificateConnectorDetails,
                ResourcePath("certificateConnectorDetails", self.resource_path),
            ),
        )

    @odata(name="userPfxCertificates", beta=True, navigation=True)
    @property
    def user_pfx_certificates(self) -> EntityCollection[UserPFXCertificate]:
        """Gets the userPfxCertificates property"""
        from office365.intune.devices.management.user_pfx_certificate import UserPFXCertificate

        return self.properties.get(
            "userPfxCertificates",
            EntityCollection[UserPFXCertificate](
                self.context, UserPFXCertificate, ResourcePath("userPfxCertificates", self.resource_path)
            ),
        )

    @odata(name="userExperienceAnalyticsAnomalySeverityOverview", beta=True)
    @property
    def user_experience_analytics_anomaly_severity_overview(
        self,
    ) -> Optional[UserExperienceAnalyticsAnomalySeverityOverview]:
        """Gets the userExperienceAnalyticsAnomalySeverityOverview property"""
        return self.properties.get("userExperienceAnalyticsAnomalySeverityOverview", None)

    @odata(name="userExperienceAnalyticsAnomaly", beta=True, navigation=True)
    @property
    def user_experience_analytics_anomaly(self) -> EntityCollection[UserExperienceAnalyticsAnomaly]:
        """Gets the userExperienceAnalyticsAnomaly property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly import (
            UserExperienceAnalyticsAnomaly,
        )

        return self.properties.get(
            "userExperienceAnalyticsAnomaly",
            EntityCollection[UserExperienceAnalyticsAnomaly](
                self.context,
                UserExperienceAnalyticsAnomaly,
                ResourcePath("userExperienceAnalyticsAnomaly", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAnomalyCorrelationGroupOverview", beta=True, navigation=True)
    @property
    def user_experience_analytics_anomaly_correlation_group_overview(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAnomalyCorrelationGroupOverview]:
        """Gets the userExperienceAnalyticsAnomalyCorrelationGroupOverview property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_correlation_group_overview import (  # noqa: E501
            UserExperienceAnalyticsAnomalyCorrelationGroupOverview,
        )

        return self.properties.get(
            "userExperienceAnalyticsAnomalyCorrelationGroupOverview",
            EntityCollection[UserExperienceAnalyticsAnomalyCorrelationGroupOverview](
                self.context,
                UserExperienceAnalyticsAnomalyCorrelationGroupOverview,
                ResourcePath("userExperienceAnalyticsAnomalyCorrelationGroupOverview", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAnomalyDevice", beta=True, navigation=True)
    @property
    def user_experience_analytics_anomaly_device(self) -> EntityCollection[UserExperienceAnalyticsAnomalyDevice]:
        """Gets the userExperienceAnalyticsAnomalyDevice property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_device import (  # noqa: E501
            UserExperienceAnalyticsAnomalyDevice,
        )

        return self.properties.get(
            "userExperienceAnalyticsAnomalyDevice",
            EntityCollection[UserExperienceAnalyticsAnomalyDevice](
                self.context,
                UserExperienceAnalyticsAnomalyDevice,
                ResourcePath("userExperienceAnalyticsAnomalyDevice", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersion", beta=True, navigation=True)
    @property
    def user_experience_analytics_app_health_application_performance_by_app_version(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsAppHealthAppPerformanceByAppVersion]:
        """Gets the userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersion property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_app_health_app_performance_by_app_version import (  # noqa: E501
            UserExperienceAnalyticsAppHealthAppPerformanceByAppVersion,
        )

        return self.properties.get(
            "userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersion",
            EntityCollection[UserExperienceAnalyticsAppHealthAppPerformanceByAppVersion](
                self.context,
                UserExperienceAnalyticsAppHealthAppPerformanceByAppVersion,
                ResourcePath("userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersion", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsBatteryHealthAppImpact", beta=True, navigation=True)
    @property
    def user_experience_analytics_battery_health_app_impact(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsBatteryHealthAppImpact]:
        """Gets the userExperienceAnalyticsBatteryHealthAppImpact property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_app_impact import (  # noqa: E501
            UserExperienceAnalyticsBatteryHealthAppImpact,
        )

        return self.properties.get(
            "userExperienceAnalyticsBatteryHealthAppImpact",
            EntityCollection[UserExperienceAnalyticsBatteryHealthAppImpact](
                self.context,
                UserExperienceAnalyticsBatteryHealthAppImpact,
                ResourcePath("userExperienceAnalyticsBatteryHealthAppImpact", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsBatteryHealthCapacityDetails", beta=True, navigation=True)
    @property
    def user_experience_analytics_battery_health_capacity_details(
        self,
    ) -> UserExperienceAnalyticsBatteryHealthCapacityDetails:
        """Gets the userExperienceAnalyticsBatteryHealthCapacityDetails property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_capacity_details import (  # noqa: E501
            UserExperienceAnalyticsBatteryHealthCapacityDetails,
        )

        return self.properties.get(
            "userExperienceAnalyticsBatteryHealthCapacityDetails",
            UserExperienceAnalyticsBatteryHealthCapacityDetails(
                self.context, ResourcePath("userExperienceAnalyticsBatteryHealthCapacityDetails", self.resource_path)
            ),
        )

    @odata(name="userExperienceAnalyticsBatteryHealthDeviceAppImpact", beta=True, navigation=True)
    @property
    def user_experience_analytics_battery_health_device_app_impact(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsBatteryHealthDeviceAppImpact]:
        """Gets the userExperienceAnalyticsBatteryHealthDeviceAppImpact property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_device_app_impact import (  # noqa: E501
            UserExperienceAnalyticsBatteryHealthDeviceAppImpact,
        )

        return self.properties.get(
            "userExperienceAnalyticsBatteryHealthDeviceAppImpact",
            EntityCollection[UserExperienceAnalyticsBatteryHealthDeviceAppImpact](
                self.context,
                UserExperienceAnalyticsBatteryHealthDeviceAppImpact,
                ResourcePath("userExperienceAnalyticsBatteryHealthDeviceAppImpact", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsBatteryHealthDevicePerformance", beta=True, navigation=True)
    @property
    def user_experience_analytics_battery_health_device_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsBatteryHealthDevicePerformance]:
        """Gets the userExperienceAnalyticsBatteryHealthDevicePerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_device_performance import (  # noqa: E501
            UserExperienceAnalyticsBatteryHealthDevicePerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsBatteryHealthDevicePerformance",
            EntityCollection[UserExperienceAnalyticsBatteryHealthDevicePerformance](
                self.context,
                UserExperienceAnalyticsBatteryHealthDevicePerformance,
                ResourcePath("userExperienceAnalyticsBatteryHealthDevicePerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsBatteryHealthDeviceRuntimeHistory", beta=True, navigation=True)
    @property
    def user_experience_analytics_battery_health_device_runtime_history(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsBatteryHealthDeviceRuntimeHistory]:
        """Gets the userExperienceAnalyticsBatteryHealthDeviceRuntimeHistory property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_device_runtime_history import (  # noqa: E501
            UserExperienceAnalyticsBatteryHealthDeviceRuntimeHistory,
        )

        return self.properties.get(
            "userExperienceAnalyticsBatteryHealthDeviceRuntimeHistory",
            EntityCollection[UserExperienceAnalyticsBatteryHealthDeviceRuntimeHistory](
                self.context,
                UserExperienceAnalyticsBatteryHealthDeviceRuntimeHistory,
                ResourcePath("userExperienceAnalyticsBatteryHealthDeviceRuntimeHistory", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsBatteryHealthModelPerformance", beta=True, navigation=True)
    @property
    def user_experience_analytics_battery_health_model_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsBatteryHealthModelPerformance]:
        """Gets the userExperienceAnalyticsBatteryHealthModelPerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_model_performance import (  # noqa: E501
            UserExperienceAnalyticsBatteryHealthModelPerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsBatteryHealthModelPerformance",
            EntityCollection[UserExperienceAnalyticsBatteryHealthModelPerformance](
                self.context,
                UserExperienceAnalyticsBatteryHealthModelPerformance,
                ResourcePath("userExperienceAnalyticsBatteryHealthModelPerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsBatteryHealthOsPerformance", beta=True, navigation=True)
    @property
    def user_experience_analytics_battery_health_os_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsBatteryHealthOsPerformance]:
        """Gets the userExperienceAnalyticsBatteryHealthOsPerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_os_performance import (  # noqa: E501
            UserExperienceAnalyticsBatteryHealthOsPerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsBatteryHealthOsPerformance",
            EntityCollection[UserExperienceAnalyticsBatteryHealthOsPerformance](
                self.context,
                UserExperienceAnalyticsBatteryHealthOsPerformance,
                ResourcePath("userExperienceAnalyticsBatteryHealthOsPerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsBatteryHealthRuntimeDetails", beta=True, navigation=True)
    @property
    def user_experience_analytics_battery_health_runtime_details(
        self,
    ) -> UserExperienceAnalyticsBatteryHealthRuntimeDetails:
        """Gets the userExperienceAnalyticsBatteryHealthRuntimeDetails property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_runtime_details import (  # noqa: E501
            UserExperienceAnalyticsBatteryHealthRuntimeDetails,
        )

        return self.properties.get(
            "userExperienceAnalyticsBatteryHealthRuntimeDetails",
            UserExperienceAnalyticsBatteryHealthRuntimeDetails(
                self.context, ResourcePath("userExperienceAnalyticsBatteryHealthRuntimeDetails", self.resource_path)
            ),
        )

    @odata(name="userExperienceAnalyticsDeviceScope", beta=True, navigation=True)
    @property
    def user_experience_analytics_device_scope(self) -> UserExperienceAnalyticsDeviceScope:
        """Gets the userExperienceAnalyticsDeviceScope property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_scope import (
            UserExperienceAnalyticsDeviceScope,
        )

        return self.properties.get(
            "userExperienceAnalyticsDeviceScope",
            UserExperienceAnalyticsDeviceScope(
                self.context, ResourcePath("userExperienceAnalyticsDeviceScope", self.resource_path)
            ),
        )

    @odata(name="userExperienceAnalyticsDeviceScopes", beta=True, navigation=True)
    @property
    def user_experience_analytics_device_scopes(self) -> EntityCollection[UserExperienceAnalyticsDeviceScope]:
        """Gets the userExperienceAnalyticsDeviceScopes property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_scope import (
            UserExperienceAnalyticsDeviceScope,
        )

        return self.properties.get(
            "userExperienceAnalyticsDeviceScopes",
            EntityCollection[UserExperienceAnalyticsDeviceScope](
                self.context,
                UserExperienceAnalyticsDeviceScope,
                ResourcePath("userExperienceAnalyticsDeviceScopes", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsDevicesWithoutCloudIdentity", beta=True, navigation=True)
    @property
    def user_experience_analytics_devices_without_cloud_identity(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsDeviceWithoutCloudIdentity]:
        """Gets the userExperienceAnalyticsDevicesWithoutCloudIdentity property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_without_cloud_identity import (  # noqa: E501
            UserExperienceAnalyticsDeviceWithoutCloudIdentity,
        )

        return self.properties.get(
            "userExperienceAnalyticsDevicesWithoutCloudIdentity",
            EntityCollection[UserExperienceAnalyticsDeviceWithoutCloudIdentity](
                self.context,
                UserExperienceAnalyticsDeviceWithoutCloudIdentity,
                ResourcePath("userExperienceAnalyticsDevicesWithoutCloudIdentity", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsDeviceTimelineEvent", beta=True, navigation=True)
    @property
    def user_experience_analytics_device_timeline_event(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsDeviceTimelineEvent]:
        """Gets the userExperienceAnalyticsDeviceTimelineEvent property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_timeline_event import (  # noqa: E501
            UserExperienceAnalyticsDeviceTimelineEvent,
        )

        return self.properties.get(
            "userExperienceAnalyticsDeviceTimelineEvent",
            EntityCollection[UserExperienceAnalyticsDeviceTimelineEvent](
                self.context,
                UserExperienceAnalyticsDeviceTimelineEvent,
                ResourcePath("userExperienceAnalyticsDeviceTimelineEvent", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsImpactingProcess", beta=True, navigation=True)
    @property
    def user_experience_analytics_impacting_process(self) -> EntityCollection[UserExperienceAnalyticsImpactingProcess]:
        """Gets the userExperienceAnalyticsImpactingProcess property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_impacting_process import (  # noqa: E501
            UserExperienceAnalyticsImpactingProcess,
        )

        return self.properties.get(
            "userExperienceAnalyticsImpactingProcess",
            EntityCollection[UserExperienceAnalyticsImpactingProcess](
                self.context,
                UserExperienceAnalyticsImpactingProcess,
                ResourcePath("userExperienceAnalyticsImpactingProcess", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsNotAutopilotReadyDevice", beta=True, navigation=True)
    @property
    def user_experience_analytics_not_autopilot_ready_device(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsNotAutopilotReadyDevice]:
        """Gets the userExperienceAnalyticsNotAutopilotReadyDevice property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_not_autopilot_ready_device import (  # noqa: E501
            UserExperienceAnalyticsNotAutopilotReadyDevice,
        )

        return self.properties.get(
            "userExperienceAnalyticsNotAutopilotReadyDevice",
            EntityCollection[UserExperienceAnalyticsNotAutopilotReadyDevice](
                self.context,
                UserExperienceAnalyticsNotAutopilotReadyDevice,
                ResourcePath("userExperienceAnalyticsNotAutopilotReadyDevice", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsRemoteConnection", beta=True, navigation=True)
    @property
    def user_experience_analytics_remote_connection(self) -> EntityCollection[UserExperienceAnalyticsRemoteConnection]:
        """Gets the userExperienceAnalyticsRemoteConnection property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_remote_connection import (  # noqa: E501
            UserExperienceAnalyticsRemoteConnection,
        )

        return self.properties.get(
            "userExperienceAnalyticsRemoteConnection",
            EntityCollection[UserExperienceAnalyticsRemoteConnection](
                self.context,
                UserExperienceAnalyticsRemoteConnection,
                ResourcePath("userExperienceAnalyticsRemoteConnection", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsResourcePerformance", beta=True, navigation=True)
    @property
    def user_experience_analytics_resource_performance(
        self,
    ) -> EntityCollection[UserExperienceAnalyticsResourcePerformance]:
        """Gets the userExperienceAnalyticsResourcePerformance property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_resource_performance import (  # noqa: E501
            UserExperienceAnalyticsResourcePerformance,
        )

        return self.properties.get(
            "userExperienceAnalyticsResourcePerformance",
            EntityCollection[UserExperienceAnalyticsResourcePerformance](
                self.context,
                UserExperienceAnalyticsResourcePerformance,
                ResourcePath("userExperienceAnalyticsResourcePerformance", self.resource_path),
            ),
        )

    @odata(name="userExperienceAnalyticsSummarizedDeviceScopes", beta=True, selectable=False)
    def user_experience_analytics_summarized_device_scopes(
        self,
    ) -> ClientResult[UserExperienceAnalyticsDeviceScopeSummary]:
        """userExperienceAnalyticsSummarizedDeviceScopes operation."""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_scope_summary import (  # noqa: E501
            UserExperienceAnalyticsDeviceScopeSummary,
        )

        return_type = ClientResult(self.context, UserExperienceAnalyticsDeviceScopeSummary())
        qry = FunctionQuery(self, "userExperienceAnalyticsSummarizedDeviceScopes", None, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="androidDeviceOwnerEnrollmentProfiles", beta=True, navigation=True)
    @property
    def android_device_owner_enrollment_profiles(self) -> EntityCollection[AndroidDeviceOwnerEnrollmentProfile]:
        """Gets the androidDeviceOwnerEnrollmentProfiles property"""
        from office365.intune.devices.enrollment.android_device_owner_enrollment_profile import (
            AndroidDeviceOwnerEnrollmentProfile,
        )

        return self.properties.get(
            "androidDeviceOwnerEnrollmentProfiles",
            EntityCollection[AndroidDeviceOwnerEnrollmentProfile](
                self.context,
                AndroidDeviceOwnerEnrollmentProfile,
                ResourcePath("androidDeviceOwnerEnrollmentProfiles", self.resource_path),
            ),
        )

    @odata(name="androidForWorkEnrollmentProfiles", beta=True, navigation=True)
    @property
    def android_for_work_enrollment_profiles(self) -> EntityCollection[AndroidForWorkEnrollmentProfile]:
        """Gets the androidForWorkEnrollmentProfiles property"""
        from office365.intune.devices.enrollment.android_for_work_enrollment_profile import (
            AndroidForWorkEnrollmentProfile,
        )

        return self.properties.get(
            "androidForWorkEnrollmentProfiles",
            EntityCollection[AndroidForWorkEnrollmentProfile](
                self.context,
                AndroidForWorkEnrollmentProfile,
                ResourcePath("androidForWorkEnrollmentProfiles", self.resource_path),
            ),
        )

    @odata(name="androidForWorkSettings", beta=True, navigation=True)
    @property
    def android_for_work_settings(self) -> AndroidForWorkSettings:
        """Gets the androidForWorkSettings property"""
        from office365.intune.devices.enrollment.android_for_work_settings import AndroidForWorkSettings

        return self.properties.get(
            "androidForWorkSettings",
            AndroidForWorkSettings(self.context, ResourcePath("androidForWorkSettings", self.resource_path)),
        )

    @odata(name="appleUserInitiatedEnrollmentProfiles", beta=True, navigation=True)
    @property
    def apple_user_initiated_enrollment_profiles(self) -> EntityCollection[AppleUserInitiatedEnrollmentProfile]:
        """Gets the appleUserInitiatedEnrollmentProfiles property"""
        from office365.intune.devices.enrollment.apple_user_initiated_enrollment_profile import (
            AppleUserInitiatedEnrollmentProfile,
        )

        return self.properties.get(
            "appleUserInitiatedEnrollmentProfiles",
            EntityCollection[AppleUserInitiatedEnrollmentProfile](
                self.context,
                AppleUserInitiatedEnrollmentProfile,
                ResourcePath("appleUserInitiatedEnrollmentProfiles", self.resource_path),
            ),
        )

    @odata(name="depOnboardingSettings", beta=True, navigation=True)
    @property
    def dep_onboarding_settings(self) -> EntityCollection[DepOnboardingSetting]:
        """Gets the depOnboardingSettings property"""
        from office365.intune.devices.enrollment.dep_onboarding_setting import DepOnboardingSetting

        return self.properties.get(
            "depOnboardingSettings",
            EntityCollection[DepOnboardingSetting](
                self.context, DepOnboardingSetting, ResourcePath("depOnboardingSettings", self.resource_path)
            ),
        )

    @odata(name="importedDeviceIdentities", beta=True, navigation=True)
    @property
    def imported_device_identities(self) -> EntityCollection[ImportedDeviceIdentity]:
        """Gets the importedDeviceIdentities property"""
        from office365.intune.devices.enrollment.imported_device_identity import ImportedDeviceIdentity

        return self.properties.get(
            "importedDeviceIdentities",
            EntityCollection[ImportedDeviceIdentity](
                self.context, ImportedDeviceIdentity, ResourcePath("importedDeviceIdentities", self.resource_path)
            ),
        )

    @odata(name="windowsAutopilotSettings", beta=True, navigation=True)
    @property
    def windows_autopilot_settings(self) -> WindowsAutopilotSettings:
        """Gets the windowsAutopilotSettings property"""
        from office365.intune.devices.management.managed.windows.autopilot_settings import WindowsAutopilotSettings

        return self.properties.get(
            "windowsAutopilotSettings",
            WindowsAutopilotSettings(self.context, ResourcePath("windowsAutopilotSettings", self.resource_path)),
        )

    @odata(name="autopilotEvents", beta=True, navigation=True)
    @property
    def autopilot_events(self) -> EntityCollection[DeviceManagementAutopilotEvent]:
        """Gets the autopilotEvents property"""
        from office365.intune.devices.management.autopilot_event import DeviceManagementAutopilotEvent

        return self.properties.get(
            "autopilotEvents",
            EntityCollection[DeviceManagementAutopilotEvent](
                self.context, DeviceManagementAutopilotEvent, ResourcePath("autopilotEvents", self.resource_path)
            ),
        )

    @odata(name="comanagementEligibleDevices", beta=True, navigation=True)
    @property
    def comanagement_eligible_devices(self) -> EntityCollection[ComanagementEligibleDevice]:
        """Gets the comanagementEligibleDevices property"""
        from office365.intune.devices.management.comanagement_eligible_device import ComanagementEligibleDevice

        return self.properties.get(
            "comanagementEligibleDevices",
            EntityCollection[ComanagementEligibleDevice](
                self.context, ComanagementEligibleDevice, ResourcePath("comanagementEligibleDevices", self.resource_path)
            ),
        )

    @odata(name="deviceConfigurationConflictSummary", beta=True, navigation=True)
    @property
    def device_configuration_conflict_summary(self) -> EntityCollection[DeviceConfigurationConflictSummary]:
        """Gets the deviceConfigurationConflictSummary property"""
        from office365.intune.devices.configurations.conflict_summary import DeviceConfigurationConflictSummary

        return self.properties.get(
            "deviceConfigurationConflictSummary",
            EntityCollection[DeviceConfigurationConflictSummary](
                self.context,
                DeviceConfigurationConflictSummary,
                ResourcePath("deviceConfigurationConflictSummary", self.resource_path),
            ),
        )

    @odata(name="deviceConfigurationUserStateSummaries", beta=True, navigation=True)
    @property
    def device_configuration_user_state_summaries(self) -> DeviceConfigurationUserStateSummary:
        """Gets the deviceConfigurationUserStateSummaries property"""
        from office365.intune.devices.configurations.user_state_summary import DeviceConfigurationUserStateSummary

        return self.properties.get(
            "deviceConfigurationUserStateSummaries",
            DeviceConfigurationUserStateSummary(
                self.context, ResourcePath("deviceConfigurationUserStateSummaries", self.resource_path)
            ),
        )

    @odata(name="deviceConfigurationRestrictedAppsViolations", beta=True, navigation=True)
    @property
    def device_configuration_restricted_apps_violations(self) -> EntityCollection[RestrictedAppsViolation]:
        """Gets the deviceConfigurationRestrictedAppsViolations property"""
        from office365.intune.devices.compliance.restricted_apps_violation import RestrictedAppsViolation

        return self.properties.get(
            "deviceConfigurationRestrictedAppsViolations",
            EntityCollection[RestrictedAppsViolation](
                self.context,
                RestrictedAppsViolation,
                ResourcePath("deviceConfigurationRestrictedAppsViolations", self.resource_path),
            ),
        )

    @odata(name="deviceConfigurationsAllManagedDeviceCertificateStates", beta=True, navigation=True)
    @property
    def device_configurations_all_managed_device_certificate_states(
        self,
    ) -> EntityCollection[ManagedAllDeviceCertificateState]:
        """Gets the deviceConfigurationsAllManagedDeviceCertificateStates property"""
        from office365.intune.devices.management.managed.all_device_certificate_state import (
            ManagedAllDeviceCertificateState,
        )

        return self.properties.get(
            "deviceConfigurationsAllManagedDeviceCertificateStates",
            EntityCollection[ManagedAllDeviceCertificateState](
                self.context,
                ManagedAllDeviceCertificateState,
                ResourcePath("deviceConfigurationsAllManagedDeviceCertificateStates", self.resource_path),
            ),
        )

    @odata(name="domainJoinConnectors", beta=True, navigation=True)
    @property
    def domain_join_connectors(self) -> EntityCollection[DeviceManagementDomainJoinConnector]:
        """Gets the domainJoinConnectors property"""
        from office365.intune.devices.management.domain_join_connector import DeviceManagementDomainJoinConnector

        return self.properties.get(
            "domainJoinConnectors",
            EntityCollection[DeviceManagementDomainJoinConnector](
                self.context,
                DeviceManagementDomainJoinConnector,
                ResourcePath("domainJoinConnectors", self.resource_path),
            ),
        )

    @odata(name="managedDeviceEncryptionStates", beta=True, navigation=True)
    @property
    def managed_device_encryption_states(self) -> EntityCollection[ManagedDeviceEncryptionState]:
        """Gets the managedDeviceEncryptionStates property"""
        from office365.intune.devices.management.managed.encryption_state import ManagedDeviceEncryptionState

        return self.properties.get(
            "managedDeviceEncryptionStates",
            EntityCollection[ManagedDeviceEncryptionState](
                self.context,
                ManagedDeviceEncryptionState,
                ResourcePath("managedDeviceEncryptionStates", self.resource_path),
            ),
        )

    @odata(name="remoteActionAudits", beta=True, navigation=True)
    @property
    def remote_action_audits(self) -> EntityCollection[RemoteActionAudit]:
        """Gets the remoteActionAudits property"""
        from office365.intune.audit.remote_action_audit import RemoteActionAudit

        return self.properties.get(
            "remoteActionAudits",
            EntityCollection[RemoteActionAudit](
                self.context, RemoteActionAudit, ResourcePath("remoteActionAudits", self.resource_path)
            ),
        )

    @odata(name="roleScopeTags", beta=True, navigation=True)
    @property
    def role_scope_tags(self) -> EntityCollection[RoleScopeTag]:
        """Gets the roleScopeTags property"""
        from office365.intune.devices.management.role_scope_tag import RoleScopeTag

        return self.properties.get(
            "roleScopeTags",
            EntityCollection[RoleScopeTag](
                self.context, RoleScopeTag, ResourcePath("roleScopeTags", self.resource_path)
            ),
        )
