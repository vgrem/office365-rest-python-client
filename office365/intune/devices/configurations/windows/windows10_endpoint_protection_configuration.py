from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.intune.devices.configurations.windows.applicationguardblockclipboardsharingtype import (  # noqa: E501
    ApplicationGuardBlockClipboardSharingType,
)
from office365.intune.devices.configurations.windows.applicationguardblockfiletransfertype import (  # noqa: E501
    ApplicationGuardBlockFileTransferType,
)
from office365.intune.devices.configurations.windows.applockerapplicationcontroltype import (  # noqa: E501
    AppLockerApplicationControlType,
)
from office365.intune.devices.configurations.windows.bit_locker_removable_drive_policy import (  # noqa: E501
    BitLockerRemovableDrivePolicy,
)
from office365.intune.devices.configurations.windows.firewallcertificaterevocationlistcheckmethodtype import (  # noqa: E501
    FirewallCertificateRevocationListCheckMethodType,
)
from office365.intune.devices.configurations.windows.firewallpacketqueueingmethodtype import (  # noqa: E501
    FirewallPacketQueueingMethodType,
)
from office365.intune.devices.configurations.windows.firewallpresharedkeyencodingmethodtype import (  # noqa: E501
    FirewallPreSharedKeyEncodingMethodType,
)
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.configurations.windows.firewall_network_profile import (
        WindowsFirewallNetworkProfile,
    )


class Windows10EndpointProtectionConfiguration(Entity):
    @odata(name="applicationGuardAllowPersistence")
    @property
    def application_guard_allow_persistence(self) -> Optional[bool]:
        """Gets the applicationGuardAllowPersistence property"""
        return self.properties.get("applicationGuardAllowPersistence", None)

    @odata(name="applicationGuardAllowPrintToLocalPrinters")
    @property
    def application_guard_allow_print_to_local_printers(self) -> Optional[bool]:
        """Gets the applicationGuardAllowPrintToLocalPrinters property"""
        return self.properties.get("applicationGuardAllowPrintToLocalPrinters", None)

    @odata(name="applicationGuardAllowPrintToNetworkPrinters")
    @property
    def application_guard_allow_print_to_network_printers(self) -> Optional[bool]:
        """Gets the applicationGuardAllowPrintToNetworkPrinters property"""
        return self.properties.get("applicationGuardAllowPrintToNetworkPrinters", None)

    @odata(name="applicationGuardAllowPrintToPDF")
    @property
    def application_guard_allow_print_to_pdf(self) -> Optional[bool]:
        """Gets the applicationGuardAllowPrintToPDF property"""
        return self.properties.get("applicationGuardAllowPrintToPDF", None)

    @odata(name="applicationGuardAllowPrintToXPS")
    @property
    def application_guard_allow_print_to_xps(self) -> Optional[bool]:
        """Gets the applicationGuardAllowPrintToXPS property"""
        return self.properties.get("applicationGuardAllowPrintToXPS", None)

    @odata(name="applicationGuardBlockClipboardSharing")
    @property
    def application_guard_block_clipboard_sharing(self) -> ApplicationGuardBlockClipboardSharingType:
        """Gets the applicationGuardBlockClipboardSharing property"""
        return self.properties.get(
            "applicationGuardBlockClipboardSharing", ApplicationGuardBlockClipboardSharingType.notConfigured
        )

    @odata(name="applicationGuardBlockFileTransfer")
    @property
    def application_guard_block_file_transfer(self) -> ApplicationGuardBlockFileTransferType:
        """Gets the applicationGuardBlockFileTransfer property"""
        return self.properties.get(
            "applicationGuardBlockFileTransfer", ApplicationGuardBlockFileTransferType.notConfigured
        )

    @odata(name="applicationGuardBlockNonEnterpriseContent")
    @property
    def application_guard_block_non_enterprise_content(self) -> Optional[bool]:
        """Gets the applicationGuardBlockNonEnterpriseContent property"""
        return self.properties.get("applicationGuardBlockNonEnterpriseContent", None)

    @odata(name="applicationGuardEnabled")
    @property
    def application_guard_enabled(self) -> Optional[bool]:
        """Gets the applicationGuardEnabled property"""
        return self.properties.get("applicationGuardEnabled", None)

    @odata(name="applicationGuardForceAuditing")
    @property
    def application_guard_force_auditing(self) -> Optional[bool]:
        """Gets the applicationGuardForceAuditing property"""
        return self.properties.get("applicationGuardForceAuditing", None)

    @odata(name="appLockerApplicationControl")
    @property
    def app_locker_application_control(self) -> AppLockerApplicationControlType:
        """Gets the appLockerApplicationControl property"""
        return self.properties.get("appLockerApplicationControl", AppLockerApplicationControlType.notConfigured)

    @odata(name="bitLockerDisableWarningForOtherDiskEncryption")
    @property
    def bit_locker_disable_warning_for_other_disk_encryption(self) -> Optional[bool]:
        """Gets the bitLockerDisableWarningForOtherDiskEncryption property"""
        return self.properties.get("bitLockerDisableWarningForOtherDiskEncryption", None)

    @odata(name="bitLockerEnableStorageCardEncryptionOnMobile")
    @property
    def bit_locker_enable_storage_card_encryption_on_mobile(self) -> Optional[bool]:
        """Gets the bitLockerEnableStorageCardEncryptionOnMobile property"""
        return self.properties.get("bitLockerEnableStorageCardEncryptionOnMobile", None)

    @odata(name="bitLockerEncryptDevice")
    @property
    def bit_locker_encrypt_device(self) -> Optional[bool]:
        """Gets the bitLockerEncryptDevice property"""
        return self.properties.get("bitLockerEncryptDevice", None)

    @odata(name="bitLockerRemovableDrivePolicy")
    @property
    def bit_locker_removable_drive_policy(self) -> BitLockerRemovableDrivePolicy:
        """Gets the bitLockerRemovableDrivePolicy property"""
        return self.properties.get("bitLockerRemovableDrivePolicy", BitLockerRemovableDrivePolicy())

    @odata(name="defenderAdditionalGuardedFolders")
    @property
    def defender_additional_guarded_folders(self) -> StringCollection:
        """Gets the defenderAdditionalGuardedFolders property"""
        return self.properties.get("defenderAdditionalGuardedFolders", StringCollection())

    @odata(name="defenderAttackSurfaceReductionExcludedPaths")
    @property
    def defender_attack_surface_reduction_excluded_paths(self) -> StringCollection:
        """Gets the defenderAttackSurfaceReductionExcludedPaths property"""
        return self.properties.get("defenderAttackSurfaceReductionExcludedPaths", StringCollection())

    @odata(name="defenderExploitProtectionXml")
    @property
    def defender_exploit_protection_xml(self) -> Optional[bytes]:
        """Gets the defenderExploitProtectionXml property"""
        return self.properties.get("defenderExploitProtectionXml", None)

    @odata(name="defenderExploitProtectionXmlFileName")
    @property
    def defender_exploit_protection_xml_file_name(self) -> Optional[str]:
        """Gets the defenderExploitProtectionXmlFileName property"""
        return self.properties.get("defenderExploitProtectionXmlFileName", None)

    @odata(name="defenderGuardedFoldersAllowedAppPaths")
    @property
    def defender_guarded_folders_allowed_app_paths(self) -> StringCollection:
        """Gets the defenderGuardedFoldersAllowedAppPaths property"""
        return self.properties.get("defenderGuardedFoldersAllowedAppPaths", StringCollection())

    @odata(name="defenderSecurityCenterBlockExploitProtectionOverride")
    @property
    def defender_security_center_block_exploit_protection_override(self) -> Optional[bool]:
        """Gets the defenderSecurityCenterBlockExploitProtectionOverride property"""
        return self.properties.get("defenderSecurityCenterBlockExploitProtectionOverride", None)

    @odata(name="firewallBlockStatefulFTP")
    @property
    def firewall_block_stateful_ftp(self) -> Optional[bool]:
        """Gets the firewallBlockStatefulFTP property"""
        return self.properties.get("firewallBlockStatefulFTP", None)

    @odata(name="firewallCertificateRevocationListCheckMethod")
    @property
    def firewall_certificate_revocation_list_check_method(self) -> FirewallCertificateRevocationListCheckMethodType:
        """Gets the firewallCertificateRevocationListCheckMethod property"""
        return self.properties.get(
            "firewallCertificateRevocationListCheckMethod",
            FirewallCertificateRevocationListCheckMethodType.deviceDefault,
        )

    @odata(name="firewallIdleTimeoutForSecurityAssociationInSeconds")
    @property
    def firewall_idle_timeout_for_security_association_in_seconds(self) -> Optional[int]:
        """Gets the firewallIdleTimeoutForSecurityAssociationInSeconds property"""
        return self.properties.get("firewallIdleTimeoutForSecurityAssociationInSeconds", None)

    @odata(name="firewallIPSecExemptionsAllowDHCP")
    @property
    def firewall_ip_sec_exemptions_allow_dhcp(self) -> Optional[bool]:
        """Gets the firewallIPSecExemptionsAllowDHCP property"""
        return self.properties.get("firewallIPSecExemptionsAllowDHCP", None)

    @odata(name="firewallIPSecExemptionsAllowICMP")
    @property
    def firewall_ip_sec_exemptions_allow_icmp(self) -> Optional[bool]:
        """Gets the firewallIPSecExemptionsAllowICMP property"""
        return self.properties.get("firewallIPSecExemptionsAllowICMP", None)

    @odata(name="firewallIPSecExemptionsAllowNeighborDiscovery")
    @property
    def firewall_ip_sec_exemptions_allow_neighbor_discovery(self) -> Optional[bool]:
        """Gets the firewallIPSecExemptionsAllowNeighborDiscovery property"""
        return self.properties.get("firewallIPSecExemptionsAllowNeighborDiscovery", None)

    @odata(name="firewallIPSecExemptionsAllowRouterDiscovery")
    @property
    def firewall_ip_sec_exemptions_allow_router_discovery(self) -> Optional[bool]:
        """Gets the firewallIPSecExemptionsAllowRouterDiscovery property"""
        return self.properties.get("firewallIPSecExemptionsAllowRouterDiscovery", None)

    @odata(name="firewallMergeKeyingModuleSettings")
    @property
    def firewall_merge_keying_module_settings(self) -> Optional[bool]:
        """Gets the firewallMergeKeyingModuleSettings property"""
        return self.properties.get("firewallMergeKeyingModuleSettings", None)

    @odata(name="firewallPacketQueueingMethod")
    @property
    def firewall_packet_queueing_method(self) -> FirewallPacketQueueingMethodType:
        """Gets the firewallPacketQueueingMethod property"""
        return self.properties.get("firewallPacketQueueingMethod", FirewallPacketQueueingMethodType.deviceDefault)

    @odata(name="firewallPreSharedKeyEncodingMethod")
    @property
    def firewall_pre_shared_key_encoding_method(self) -> FirewallPreSharedKeyEncodingMethodType:
        """Gets the firewallPreSharedKeyEncodingMethod property"""
        return self.properties.get(
            "firewallPreSharedKeyEncodingMethod", FirewallPreSharedKeyEncodingMethodType.deviceDefault
        )

    @odata(name="firewallProfileDomain")
    @property
    def firewall_profile_domain(self) -> Optional[WindowsFirewallNetworkProfile]:
        """Gets the firewallProfileDomain property"""
        return self.properties.get("firewallProfileDomain", None)

    @odata(name="firewallProfilePrivate")
    @property
    def firewall_profile_private(self) -> Optional[WindowsFirewallNetworkProfile]:
        """Gets the firewallProfilePrivate property"""
        return self.properties.get("firewallProfilePrivate", None)

    @odata(name="firewallProfilePublic")
    @property
    def firewall_profile_public(self) -> Optional[WindowsFirewallNetworkProfile]:
        """Gets the firewallProfilePublic property"""
        return self.properties.get("firewallProfilePublic", None)

    @odata(name="smartScreenBlockOverrideForFiles")
    @property
    def smart_screen_block_override_for_files(self) -> Optional[bool]:
        """Gets the smartScreenBlockOverrideForFiles property"""
        return self.properties.get("smartScreenBlockOverrideForFiles", None)

    @odata(name="smartScreenEnableInShell")
    @property
    def smart_screen_enable_in_shell(self) -> Optional[bool]:
        """Gets the smartScreenEnableInShell property"""
        return self.properties.get("smartScreenEnableInShell", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Windows10EndpointProtectionConfiguration"
