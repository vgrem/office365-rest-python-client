from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.key_value_pair import KeyValuePair
from office365.runtime.types.odata_property import odata, version


@version("beta")
class MicrosoftTunnelConfiguration(Entity):
    @odata(name="advancedSettings")
    @property
    def advanced_settings(self) -> ClientValueCollection[KeyValuePair]:
        """Gets the advancedSettings property"""
        return self.properties.get("advancedSettings", ClientValueCollection[KeyValuePair](KeyValuePair))

    @odata(name="defaultDomainSuffix")
    @property
    def default_domain_suffix(self) -> Optional[str]:
        """Gets the defaultDomainSuffix property"""
        return self.properties.get("defaultDomainSuffix", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="disableUdpConnections")
    @property
    def disable_udp_connections(self) -> Optional[bool]:
        """Gets the disableUdpConnections property"""
        return self.properties.get("disableUdpConnections", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="dnsServers")
    @property
    def dns_servers(self) -> StringCollection:
        """Gets the dnsServers property"""
        return self.properties.get("dnsServers", StringCollection())

    @odata(name="ipv6Network")
    @property
    def ipv6_network(self) -> Optional[str]:
        """Gets the ipv6Network property"""
        return self.properties.get("ipv6Network", None)

    @odata(name="lastUpdateDateTime")
    @property
    def last_update_date_time(self) -> Optional[datetime]:
        """Gets the lastUpdateDateTime property"""
        return self.properties.get("lastUpdateDateTime", None)

    @odata(name="listenPort")
    @property
    def listen_port(self) -> Optional[int]:
        """Gets the listenPort property"""
        return self.properties.get("listenPort", None)

    @odata(name="network")
    @property
    def network(self) -> Optional[str]:
        """Gets the network property"""
        return self.properties.get("network", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="routeExcludes")
    @property
    def route_excludes(self) -> StringCollection:
        """Gets the routeExcludes property"""
        return self.properties.get("routeExcludes", StringCollection())

    @odata(name="routeIncludes")
    @property
    def route_includes(self) -> StringCollection:
        """Gets the routeIncludes property"""
        return self.properties.get("routeIncludes", StringCollection())

    @odata(name="routesExclude")
    @property
    def routes_exclude(self) -> StringCollection:
        """Gets the routesExclude property"""
        return self.properties.get("routesExclude", StringCollection())

    @odata(name="routesInclude")
    @property
    def routes_include(self) -> StringCollection:
        """Gets the routesInclude property"""
        return self.properties.get("routesInclude", StringCollection())

    @odata(name="splitDNS")
    @property
    def split_dns(self) -> StringCollection:
        """Gets the splitDNS property"""
        return self.properties.get("splitDNS", StringCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftTunnelConfiguration"
