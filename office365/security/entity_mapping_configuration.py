from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.account_entity_mapping import AccountEntityMapping
from office365.security.amazon_resource_entity_mapping import AmazonResourceEntityMapping
from office365.security.azure_resource_entity_mapping import AzureResourceEntityMapping
from office365.security.cloud_application_entity_mapping import CloudApplicationEntityMapping
from office365.security.dns_entity_mapping import DnsEntityMapping
from office365.security.file_entity_mapping import FileEntityMapping
from office365.security.google_cloud_resource_entity_mapping import GoogleCloudResourceEntityMapping
from office365.security.group_entity_mapping import SecurityGroupEntityMapping
from office365.security.host_entity_mapping import HostEntityMapping
from office365.security.ip_entity_mapping import IpEntityMapping
from office365.security.mail_cluster_entity_mapping import MailClusterEntityMapping
from office365.security.mail_message_entity_mapping import MailMessageEntityMapping
from office365.security.mailbox_entity_mapping import MailboxEntityMapping
from office365.security.o_auth_application_entity_mapping import OAuthApplicationEntityMapping
from office365.security.process_entity_mapping import ProcessEntityMapping
from office365.security.registry_value_entity_mapping import RegistryValueEntityMapping
from office365.security.url_entity_mapping import UrlEntityMapping


@dataclass
class EntityMappingConfiguration(ClientValue):
    accounts: ClientValueCollection[AccountEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(AccountEntityMapping)
    )
    amazonResources: ClientValueCollection[AmazonResourceEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(AmazonResourceEntityMapping)
    )
    azureResources: ClientValueCollection[AzureResourceEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(AzureResourceEntityMapping)
    )
    cloudApplications: ClientValueCollection[CloudApplicationEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(CloudApplicationEntityMapping)
    )
    dns: ClientValueCollection[DnsEntityMapping] = field(default_factory=lambda: ClientValueCollection(DnsEntityMapping))
    files: ClientValueCollection[FileEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(FileEntityMapping)
    )
    googleCloudResources: ClientValueCollection[GoogleCloudResourceEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(GoogleCloudResourceEntityMapping)
    )
    hosts: ClientValueCollection[HostEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(HostEntityMapping)
    )
    ips: ClientValueCollection[IpEntityMapping] = field(default_factory=lambda: ClientValueCollection(IpEntityMapping))
    mailboxes: ClientValueCollection[MailboxEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(MailboxEntityMapping)
    )
    mailClusters: ClientValueCollection[MailClusterEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(MailClusterEntityMapping)
    )
    mailMessages: ClientValueCollection[MailMessageEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(MailMessageEntityMapping)
    )
    oAuthApplications: ClientValueCollection[OAuthApplicationEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(OAuthApplicationEntityMapping)
    )
    processes: ClientValueCollection[ProcessEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(ProcessEntityMapping)
    )
    registryValues: ClientValueCollection[RegistryValueEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(RegistryValueEntityMapping)
    )
    securityGroups: ClientValueCollection[SecurityGroupEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(SecurityGroupEntityMapping)
    )
    urls: ClientValueCollection[UrlEntityMapping] = field(
        default_factory=lambda: ClientValueCollection(UrlEntityMapping)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EntityMappingConfiguration"
