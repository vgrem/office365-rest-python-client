# Intune endpoints and the beta service

Intune is the one workload on Microsoft Graph whose admin portal is served from `beta`, and
the two service roots do not carry the same surface. Read from the CSDL snapshots this
repository ships (`generator/metadata/Graph.xml` and `GraphBeta.xml`):

| Root | `v1.0` segments | `beta` segments |
|---|---|---|
| `deviceManagement` | 57 | 173 |
| `deviceAppManagement` | 15 | 27 |

Every `v1.0` segment also exists in `beta`, so the preview root is a strict superset: 128
segments across the two roots have no stable counterpart at all, and 81 of them answer a
plain read today.

That is why this page exists. `office365.intune` models the `v1.0` surface: 70 members (55
on `device_management`, 15 on `device_app_management`), and every one of them addresses a
segment `v1.0` carries. Settings Catalog, assignment filters, the script family, scope
tags, update rings, Autopilot profiles and policy sets have no member to call — not
because the call is wrong, but because the model has never been widened to the beta
snapshot. Widening it is a model change; the version switch below only decides which root
an existing member is addressed against.

## Switching the service root

```python
from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion

client = GraphClient(tenant="contoso.onmicrosoft.com", version=GraphVersion.BETA).with_client_secret(
    client_id, client_secret
)
client.pending_request().service_root_url  # 'https://graph.microsoft.com/beta'

client.version = GraphVersion.V1  # retargets the pending request; 'https://graph.microsoft.com/v1.0'
```

The version belongs to the client's request, not to the model. `device_management` is the
same object on either client, and the same call answers from whichever root the client
addresses. `GraphClient()` defaults to `v1.0`.

A segment a root does not carry does not raise: the service answers `400 BadRequest` with
`Resource not found for the segment '<name>'`. That is the signal the tables below record.

## What the library reaches today

70 members, one row each. *Measured* is what this tenant answered on the two roots — see
[Reading the answers](#reading-the-answers) for the four values.

| Endpoint | Library member on the client | Measured |
|---|---|---|
| `deviceManagement/detectedApps` | `device_management.detected_apps` | both |
| `deviceManagement/deviceCategories` | `device_management.device_categories` | both |
| `deviceManagement/deviceCompliancePolicies` | `device_management.device_compliance_policies` | both |
| `deviceManagement/deviceCompliancePolicyDeviceStateSummary` | `device_management.device_compliance_policy_device_state_summary` | both |
| `deviceManagement/deviceCompliancePolicySettingStateSummaries` | `device_management.device_compliance_policy_setting_state_summaries` | both |
| `deviceManagement/deviceConfigurationDeviceStateSummaries` | `device_management.device_configuration_device_state_summaries` | both |
| `deviceManagement/deviceConfigurations` | `device_management.device_configurations` | both |
| `deviceManagement/managedDeviceOverview` | `device_management.managed_device_overview` | both |
| `deviceManagement/managedDevices` | `device_management.managed_devices` | both |
| `deviceManagement/notificationMessageTemplates` | `device_management.notification_message_templates` | both |
| `deviceManagement/softwareUpdateStatusSummary` | `device_management.software_update_status_summary` | both |
| `deviceManagement/troubleshootingEvents` | `device_management.troubleshooting_events` | both |
| `deviceManagement/userExperienceAnalyticsAppHealthApplicationPerformance` | `device_management.user_experience_analytics_app_health_application_performance` | both |
| `deviceManagement/userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDetails` | `device_management.user_experience_analytics_app_health_application_performance_by_app_version_details` | both |
| `deviceManagement/userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersionDeviceId` | `device_management.user_experience_analytics_app_health_application_performance_by_app_version_device_id` | both |
| `deviceManagement/userExperienceAnalyticsAppHealthDeviceModelPerformance` | `device_management.user_experience_analytics_app_health_device_model_performance` | both |
| `deviceManagement/userExperienceAnalyticsAppHealthDevicePerformance` | `device_management.user_experience_analytics_app_health_device_performance` | both |
| `deviceManagement/userExperienceAnalyticsAppHealthDevicePerformanceDetails` | `device_management.user_experience_analytics_app_health_device_performance_details` | both |
| `deviceManagement/userExperienceAnalyticsAppHealthOverview` | `device_management.user_experience_analytics_app_health_overview` | both |
| `deviceManagement/userExperienceAnalyticsBaselines` | `device_management.user_experience_analytics_baselines` | both |
| `deviceManagement/userExperienceAnalyticsDevicePerformance` | `device_management.user_experience_analytics_device_performance` | both |
| `deviceManagement/userExperienceAnalyticsDeviceScores` | `device_management.user_experience_analytics_device_scores` | both |
| `deviceManagement/userExperienceAnalyticsDeviceStartupProcessPerformance` | `device_management.user_experience_analytics_device_startup_process_performance` | both |
| `deviceManagement/userExperienceAnalyticsMetricHistory` | `device_management.user_experience_analytics_metric_history` | both |
| `deviceManagement/userExperienceAnalyticsModelScores` | `device_management.user_experience_analytics_model_scores` | both |
| `deviceManagement/userExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric` | `device_management.user_experience_analytics_work_from_anywhere_hardware_readiness_metric` | both |
| `deviceManagement/userExperienceAnalyticsWorkFromAnywhereModelPerformance` | `device_management.user_experience_analytics_work_from_anywhere_model_performance` | both |
| `deviceManagement/windowsMalwareInformation` | `device_management.windows_malware_information` | both |
| `deviceAppManagement/androidManagedAppProtections` | `device_app_management.android_managed_app_protections` | refused |
| `deviceAppManagement/defaultManagedAppProtections` | `device_app_management.default_managed_app_protections` | refused |
| `deviceAppManagement/iosManagedAppProtections` | `device_app_management.ios_managed_app_protections` | refused |
| `deviceAppManagement/managedAppPolicies` | `device_app_management.managed_app_policies` | refused |
| `deviceAppManagement/managedAppRegistrations` | `device_app_management.managed_app_registrations` | refused |
| `deviceAppManagement/managedAppStatuses` | `device_app_management.managed_app_statuses` | refused |
| `deviceAppManagement/managedEBooks` | `device_app_management.managed_e_books` | refused |
| `deviceAppManagement/mdmWindowsInformationProtectionPolicies` | `device_app_management.mdm_windows_information_protection_policies` | refused |
| `deviceAppManagement/mobileAppCategories` | `device_app_management.mobile_app_categories` | refused |
| `deviceAppManagement/mobileAppConfigurations` | `device_app_management.mobile_app_configurations` | refused |
| `deviceAppManagement/mobileAppRelationships` | `device_app_management.mobile_app_relationships` | refused |
| `deviceAppManagement/mobileApps` | `device_app_management.mobile_apps` | refused |
| `deviceAppManagement/targetedManagedAppConfigurations` | `device_app_management.targeted_managed_app_configurations` | refused |
| `deviceAppManagement/vppTokens` | `device_app_management.vpp_tokens` | refused |
| `deviceAppManagement/windowsInformationProtectionPolicies` | `device_app_management.windows_information_protection_policies` | refused |
| `deviceManagement/applePushNotificationCertificate` | `device_management.apple_push_notification_certificate` | refused |
| `deviceManagement/auditEvents` | `device_management.audit_events` | refused |
| `deviceManagement/complianceManagementPartners` | `device_management.compliance_management_partners` | refused |
| `deviceManagement/conditionalAccessSettings` | `device_management.conditional_access_settings` | refused |
| `deviceManagement/deviceEnrollmentConfigurations` | `device_management.device_enrollment_configurations` | refused |
| `deviceManagement/deviceManagementPartners` | `device_management.device_management_partners` | refused |
| `deviceManagement/exchangeConnectors` | `device_management.exchange_connectors` | refused |
| `deviceManagement/importedWindowsAutopilotDeviceIdentities` | `device_management.imported_windows_autopilot_device_identities` | refused |
| `deviceManagement/mobileThreatDefenseConnectors` | `device_management.mobile_threat_defense_connectors` | refused |
| `deviceManagement/remoteAssistancePartners` | `device_management.remote_assistance_partners` | refused |
| `deviceManagement/resourceOperations` | `device_management.resource_operations` | refused |
| `deviceManagement/roleAssignments` | `device_management.role_assignments` | refused |
| `deviceManagement/roleDefinitions` | `device_management.role_definitions` | refused |
| `deviceManagement/termsAndConditions` | `device_management.terms_and_conditions` | refused |
| `deviceManagement/virtualEndpoint` | `device_management.virtual_endpoint` | refused |
| `deviceManagement/windowsAutopilotDeviceIdentities` | `device_management.windows_autopilot_device_identities` | refused |
| `deviceManagement/windowsInformationProtectionAppLearningSummaries` | `device_management.windows_information_protection_app_learning_summaries` | refused |
| `deviceManagement/windowsInformationProtectionNetworkLearningSummaries` | `device_management.windows_information_protection_network_learning_summaries` | refused |
| `deviceManagement/iosUpdateStatuses` | `device_management.ios_update_statuses` | unverifiable |
| `deviceManagement/mobileAppTroubleshootingEvents` | `device_management.mobile_app_troubleshooting_events` | unverifiable |
| `deviceManagement/reports` | `device_management.reports` | unverifiable |
| `deviceManagement/userExperienceAnalyticsCategories` | `device_management.user_experience_analytics_categories` | unverifiable |
| `deviceManagement/userExperienceAnalyticsDeviceStartupHistory` | `device_management.user_experience_analytics_device_startup_history` | unverifiable |
| `deviceManagement/userExperienceAnalyticsDeviceStartupProcesses` | `device_management.user_experience_analytics_device_startup_processes` | unverifiable |
| `deviceManagement/userExperienceAnalyticsOverview` | `device_management.user_experience_analytics_overview` | unverifiable |
| `deviceManagement/userExperienceAnalyticsScoreHistory` | `device_management.user_experience_analytics_score_history` | unverifiable |
| `deviceManagement/userExperienceAnalyticsWorkFromAnywhereMetrics` | `device_management.user_experience_analytics_work_from_anywhere_metrics` | unverifiable |

All 70 segments are `v1.0` segments. The version switch cannot, today, reach a single
segment the stable root does not carry: the model has no `beta`-only member to try.

## The beta-only surface

The 36 families the migration plan needs, none of which `v1.0` carries:

| Endpoint | Measured |
|---|---|
| `deviceManagement/configurationPolicies` | beta only |
| `deviceManagement/configurationPolicyTemplates` | beta only |
| `deviceManagement/configurationSettings` | beta only |
| `deviceManagement/configurationCategories` | beta only |
| `deviceManagement/compliancePolicies` | beta only |
| `deviceManagement/assignmentFilters` | beta only |
| `deviceManagement/roleScopeTags` | refused |
| `deviceManagement/deviceManagementScripts` | refused |
| `deviceManagement/deviceShellScripts` | refused |
| `deviceManagement/deviceHealthScripts` | refused |
| `deviceManagement/deviceComplianceScripts` | refused |
| `deviceManagement/deviceCustomAttributeShellScripts` | refused |
| `deviceManagement/intents` | beta only |
| `deviceManagement/windowsFeatureUpdateProfiles` | beta only |
| `deviceManagement/windowsQualityUpdateProfiles` | beta only |
| `deviceManagement/windowsQualityUpdatePolicies` | beta only |
| `deviceManagement/windowsDriverUpdateProfiles` | beta only |
| `deviceManagement/windowsUpdateCatalogItems` | beta only |
| `deviceManagement/groupPolicyConfigurations` | beta only |
| `deviceManagement/groupPolicyUploadedDefinitionFiles` | beta only |
| `deviceManagement/windowsAutopilotDeploymentProfiles` | refused |
| `deviceManagement/windowsAutopilotSettings` | refused |
| `deviceManagement/reusablePolicySettings` | beta only |
| `deviceManagement/templates` | beta only |
| `deviceManagement/appleUserInitiatedEnrollmentProfiles` | refused |
| `deviceManagement/depOnboardingSettings` | refused |
| `deviceManagement/androidForWorkEnrollmentProfiles` | beta only |
| `deviceManagement/androidManagedStoreAccountEnterpriseSettings` | beta only |
| `deviceManagement/comanagedDevices` | beta only |
| `deviceManagement/comanagementEligibleDevices` | beta only |
| `deviceAppManagement/policySets` | beta only |
| `deviceAppManagement/mobileAppCatalogPackages` | refused |
| `deviceAppManagement/managedEBookCategories` | refused |
| `deviceAppManagement/windowsManagedAppProtections` | refused |
| `deviceAppManagement/windowsManagementApp` | refused |
| `deviceAppManagement/windowsInformationProtectionWipeActions` | refused |

21 of them answer `200` on `beta` with the delegated scopes this tenant
already holds — Settings Catalog (`configurationPolicies`,
`configurationPolicyTemplates`, `configurationSettings`, `configurationCategories`),
compliance policies, assignment filters, intents, the Windows update profile family,
group policy configurations, reusable policy settings and templates. The other
15 are refused, each naming the scope it wants (see
[What the refusals name](#what-the-refusals-name)). The 81 readable preview segments in
total are listed in the
[appendix](#appendix-the-130-segments-the-library-does-not-reach).

## Reading the answers

Every one of the 200 segments was asked once per root, with the delegated client, as a
plain collection read:

| Answer | Segments | Meaning |
|---|---|---|
| `200` on both roots | 30 | the classic surface, reachable today |
| `200` on `beta`, `400` on `v1.0` | 81 | preview-only — the root is the only difference |
| `403` on both roots | 33 | the segment exists on both; the caller's permissions do not reach it |
| `403` on `beta`, `400` on `v1.0` | 27 | preview-only *and* not authorised |
| `400` on both roots | 19 | declared as a navigation, but not addressable as a plain `GET` |
| `404` | 5 | a singleton or a key-addressed resource, not a collection |
| `5xx` | 5 | the service itself; unverifiable from here |

The last two rows are why `unverifiable` appears in the tables above: neither root
answered with a collection, and neither refusal is a statement about the model.

Two shapes of `403` show up, and they are worth telling apart:

* Graph's own refusal names the scope set, e.g. *"Application is not authorized to
  perform this operation. Application must have one of the following scopes:
  DeviceManagementScripts.Read.All, DeviceManagementScripts.ReadWrite.All"*. Intune
  answers this way for the overwhelming majority of the 60 refused segments.
* A handful (`virtualEndpoint`, `remoteAssistanceSettings`, `cloudCertificationAuthority`,
  `managedDeviceWindowsOSImages`, `deviceComplianceScripts`, `deviceHealthScripts`) refuse
  with `accessDenied`, `UnknownError` or a bare `403`, naming no scope. Nothing can be
  concluded about their permissions from here.

## What the refusals name

Grouping the 54 refusals that do publish a scope list gives six families. The names are
Intune's own spelling, including the doubled
`DeviceManagementServiceConfiguration.Read.All` / `DeviceManagementServiceConfig.Read.All`
pair:

| Scopes the service wants | Segments | Plan targets it covers |
|---|---|---|
| `DeviceManagementApps.Read.All` or `…ReadWrite.All` | 26 | `mobileApps`, `managedAppPolicies`, `windowsManagedAppProtections`, `auditEvents`, the MAM policies |
| `DeviceManagementServiceConfig.Read.All` or `…ReadWrite.All` | 18 | Autopilot profiles and settings, `appleUserInitiatedEnrollmentProfiles`, `depOnboardingSettings` |
| `DeviceManagementRBAC.Read.All` or `…ReadWrite.All` | 5 | `roleScopeTags`, `roleAssignments`, `roleDefinitions` |
| `DeviceManagementScripts.Read.All` or `…ReadWrite.All` | 3 | `deviceManagementScripts`, `deviceShellScripts`, `deviceCustomAttributeShellScripts` |
| `DeviceManagementManagedDevices.PrivilegedOperations.All` | 1 | `hardwarePasswordDetails` |
| `DeviceManagementApps.*` **and** `DeviceManagementServiceConfig.*` | 1 | `vppTokens` |

The tenant used for this measurement holds two Intune scopes in its delegated token:
`DeviceManagementConfiguration.Read.All` and `DeviceManagementManagedDevices.ReadWrite.All`.
That is exactly why the Settings Catalog families answer `200` while the six families above
answer `403` — and why an app-only token answers `403 Application is not authorized` on the
whole workload: no Intune app role is assigned at all.

`office365.intune` declares none of these scopes. The permission ratchet records the
generated Intune methods as debt (`intune: 77`), not as declarations.

## What this page cannot say

* **One tenant, one date.** Every number is a `GET` against a single tenant on 2026-11-07,
  with a delegated user who is a directory reader. Another tenant, another licence mix,
  another set of role assignments, a different answer.
* **A `403` prices nothing.** It names refusal, not the missing grant; only the token's
  `scp` or `oauth2PermissionGrants` can say what the caller actually holds, and only the
  message above can say what the service wanted.
* **A `500`/`504`/`404` is not evidence about the model.** Licensing-gated families
  (Intune Suite, Endpoint Privilege Management, Remote Help, Tunnel) live in that group
  here, so their models are neither proven present nor proven missing.
* **`beta` is preview.** A segment that answers today may change shape; that is why
  widening the model to `GraphBeta.xml` is a separate, marker-applied step rather than a
  silent flip of the snapshot path.

## Appendix: the 130 segments the library does not reach

Grouped by the answer measured on `beta`.

Answer `200` on `beta`, `400` on `v1.0` (81) — the surface a beta pass would add:

`advancedThreatProtectionOnboardingStateSummary`, `androidDeviceOwnerEnrollmentProfiles`, `androidForWorkEnrollmentProfiles`, `androidForWorkSettings`, `androidManagedStoreAccountEnterpriseSettings`, `assignmentFilters`, `autopilotEvents`, `cartToClassAssociations`, `categories`, `chromeOSOnboardingSettings`, `cloudPCConnectivityIssues`, `comanagedDevices`, `comanagementEligibleDevices`, `complianceCategories`, `compliancePolicies`, `complianceSettings`, `configManagerCollections`, `configurationCategories`, `configurationPolicies`, `configurationPolicyTemplates`, `configurationSettings`, `derivedCredentials`, `deviceConfigurationConflictSummary`, `deviceConfigurationRestrictedAppsViolations`, `deviceConfigurationUserStateSummaries`, `deviceConfigurationsAllManagedDeviceCertificateStates`, `domainJoinConnectors`, `elevationRequests`, `embeddedSIMActivationCodePools`, `endpointPrivilegeManagementProvisioningStatus`, `enterpriseCodeSigningCertificates`, `groupPolicyCategories`, `groupPolicyConfigurations`, `groupPolicyDefinitionFiles`, `groupPolicyDefinitions`, `groupPolicyMigrationReports`, `groupPolicyObjectFiles`, `groupPolicyUploadedDefinitionFiles`, `hardwareConfigurations`, `intents`, `macOSSoftwareUpdateAccountSummaries`, `managedDeviceCleanupRules`, `managedDeviceEncryptionStates`, `microsoftTunnelConfigurations`, `microsoftTunnelHealthThresholds`, `microsoftTunnelServerLogCollectionResponses`, `microsoftTunnelSites`, `ndesConnectors`, `operationApprovalRequests`, `policySets`, `privilegeManagementElevations`, `remoteActionAudits`, `resourceAccessProfiles`, `reusablePolicySettings`, `reusableSettings`, `settingDefinitions`, `symantecCodeSigningCertificate`, `templates`, `userExperienceAnalyticsAnomaly`, `userExperienceAnalyticsAppHealthApplicationPerformanceByAppVersion`, `userExperienceAnalyticsBatteryHealthAppImpact`, `userExperienceAnalyticsBatteryHealthCapacityDetails`, `userExperienceAnalyticsBatteryHealthDeviceAppImpact`, `userExperienceAnalyticsBatteryHealthDevicePerformance`, `userExperienceAnalyticsBatteryHealthDeviceRuntimeHistory`, `userExperienceAnalyticsBatteryHealthModelPerformance`, `userExperienceAnalyticsBatteryHealthOsPerformance`, `userExperienceAnalyticsBatteryHealthRuntimeDetails`, `userExperienceAnalyticsDeviceMetricHistory`, `userExperienceAnalyticsDeviceScopes`, `userExperienceAnalyticsDeviceTimelineEvent`, `userExperienceAnalyticsDevicesWithoutCloudIdentity`, `userExperienceAnalyticsNotAutopilotReadyDevice`, `userExperienceAnalyticsResourcePerformance`, `userPfxCertificates`, `windowsDriverUpdateProfiles`, `windowsFeatureUpdateProfiles`, `windowsQualityUpdatePolicies`, `windowsQualityUpdateProfiles`, `windowsUpdateCatalogItems`, `zebraFotaDeployments`

Refused on at least one root (27) — needs a scope from the table above:

`appleUserInitiatedEnrollmentProfiles`, `cloudCertificationAuthority`, `depOnboardingSettings`, `deviceAppManagementTasks`, `deviceComplianceScripts`, `deviceCustomAttributeShellScripts`, `deviceHealthScripts`, `deviceManagementScripts`, `deviceShellScripts`, `exchangeOnPremisesPolicy`, `hardwarePasswordDetails`, `importedDeviceIdentities`, `intuneBrandingProfiles`, `iosLobAppProvisioningConfigurations`, `managedDeviceWindowsOSImages`, `managedEBookCategories`, `mobileAppCatalogPackages`, `operationApprovalPolicies`, `remoteAssistanceSettings`, `roleScopeTags`, `wdacSupplementalPolicies`, `windowsAutopilotDeploymentProfiles`, `windowsAutopilotSettings`, `windowsInformationProtectionDeviceRegistrations`, `windowsInformationProtectionWipeActions`, `windowsManagedAppProtections`, `windowsManagementApp`

Neither root answered with a collection (20) — `400` on both, or `404`/`5xx` on `beta`:

`androidAppConfigurationSchema`, `androidForWorkAppConfigurationSchemas`, `androidManagedStoreAppConfigurationSchemas`, `certificateConnectorDetails`, `cloudCertificationAuthorityLeafCertificate`, `dataSharingConsents`, `exchangeOnPremisesPolicies`, `hardwarePasswordInfo`, `monitoring`, `serviceNowConnections`, `templateInsights`, `templateSettings`, `tenantAttachRBAC`, `userExperienceAnalyticsAnomalyCorrelationGroupOverview`, `userExperienceAnalyticsAnomalyDevice`, `userExperienceAnalyticsDeviceScope`, `userExperienceAnalyticsImpactingProcess`, `userExperienceAnalyticsRemoteConnection`, `zebraFotaArtifacts`, `zebraFotaConnector`

## How the numbers were produced

Three sources, joined on the segment name:

1. `generator/metadata/Graph.xml` and `GraphBeta.xml` — which navigation properties
   `deviceManagement` and `deviceAppManagement` declare, per root.
2. `office365.intune` — which Python member addresses each segment, by asking
   `DeviceManagement` / `DeviceAppManagement` whether it has the snake-cased member.
3. One live `GET` per segment per root with the delegated client, capturing only the
   status code and the first bytes of the body.
