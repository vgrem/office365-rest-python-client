from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.intune.devices.management.exchangeconnectors.status import DeviceManagementExchangeConnectorStatus
from office365.intune.devices.management.exchangeconnectors.type import DeviceManagementExchangeConnectorType
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.intune.devices.management.exchangeconnectors.synctype import DeviceManagementExchangeConnectorSyncType


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
        return self.properties.get("status", DeviceManagementExchangeConnectorStatus.none)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementExchangeConnector"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All"],
    )
    def sync(self, sync_type: DeviceManagementExchangeConnectorSyncType) -> Self:
        """sync operation.

        Args:
            sync_type (DeviceManagementExchangeConnectorSyncType):
                syncType parameter
        """
        qry = ServiceOperationQuery(self, "sync", None, {"syncType": sync_type}, None, None)
        self.context.add_query(qry)
        return self
