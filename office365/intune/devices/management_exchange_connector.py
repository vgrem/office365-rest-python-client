from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.exchangeconnectors.status import (
        DeviceManagementExchangeConnectorStatus,
    )
    from office365.intune.devices.management.exchangeconnectors.type import (
        DeviceManagementExchangeConnectorType,
    )


class DeviceManagementExchangeConnector(Entity):
    @odata(name="connectorServerName")
    @property
    def connector_server_name(self) -> Optional[str]:
        """Gets the connectorServerName property"""
        return self.properties.get("connectorServerName", None)

    @odata(name="exchangeAlias")
    @property
    def exchange_alias(self) -> Optional[str]:
        """Gets the exchangeAlias property"""
        return self.properties.get("exchangeAlias", None)

    @odata(name="exchangeConnectorType")
    @property
    def exchange_connector_type(self) -> DeviceManagementExchangeConnectorType:
        """Gets the exchangeConnectorType property"""
        from office365.intune.devices.management.exchangeconnectors.type import (
            DeviceManagementExchangeConnectorType,
        )

        return self.properties.get("exchangeConnectorType", DeviceManagementExchangeConnectorType.onPremises)

    @odata(name="exchangeOrganization")
    @property
    def exchange_organization(self) -> Optional[str]:
        """Gets the exchangeOrganization property"""
        return self.properties.get("exchangeOrganization", None)

    @odata(name="lastSyncDateTime")
    @property
    def last_sync_date_time(self) -> Optional[datetime]:
        """Gets the lastSyncDateTime property"""
        return self.properties.get("lastSyncDateTime", datetime.min)

    @odata(name="primarySmtpAddress")
    @property
    def primary_smtp_address(self) -> Optional[str]:
        """Gets the primarySmtpAddress property"""
        return self.properties.get("primarySmtpAddress", None)

    @odata(name="serverName")
    @property
    def server_name(self) -> Optional[str]:
        """Gets the serverName property"""
        return self.properties.get("serverName", None)

    @odata(name="status")
    @property
    def status(self) -> DeviceManagementExchangeConnectorStatus:
        """Gets the status property"""
        from office365.intune.devices.management.exchangeconnectors.status import (
            DeviceManagementExchangeConnectorStatus,
        )

        return self.properties.get("status", DeviceManagementExchangeConnectorStatus.none)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementExchangeConnector"
