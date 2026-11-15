from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.alerts.entitymappings.account import AccountEntityMapping
from office365.security.alerts.entitymappings.amazon_resource import AmazonResourceEntityMapping
from office365.security.alerts.entitymappings.azure_resource import AzureResourceEntityMapping
from office365.security.alerts.entitymappings.cloud_application import CloudApplicationEntityMapping
from office365.security.alerts.entitymappings.dns import DnsEntityMapping
from office365.security.alerts.entitymappings.file import FileEntityMapping
from office365.security.alerts.entitymappings.google_cloud_resource import GoogleCloudResourceEntityMapping
from office365.security.alerts.entitymappings.group import SecurityGroupEntityMapping
from office365.security.alerts.entitymappings.host import HostEntityMapping
from office365.security.alerts.entitymappings.ip import IpEntityMapping
from office365.security.alerts.entitymappings.mail_cluster import MailClusterEntityMapping
from office365.security.alerts.entitymappings.mail_message import MailMessageEntityMapping
from office365.security.alerts.entitymappings.mailbox import MailboxEntityMapping
from office365.security.alerts.entitymappings.o_auth_application import OAuthApplicationEntityMapping
from office365.security.alerts.entitymappings.process import ProcessEntityMapping
from office365.security.alerts.entitymappings.registry_value import RegistryValueEntityMapping
from office365.security.alerts.entitymappings.url import UrlEntityMapping


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
