from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.multigeo.service.move_job_entity_data import MoveJobEntityData


class SiteMoveJobEntityData(MoveJobEntityData):
    """"""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.MultiGeo.Service.SiteMoveJobEntityData"

    @odata(name="EnableRestoreOnSiteToMove", beta=True)
    @property
    def enable_restore_on_site_to_move(self) -> Optional[bool]:
        """Gets the EnableRestoreOnSiteToMove property"""
        return self.properties.get("EnableRestoreOnSiteToMove", None)

    @odata(name="EnableSiteToMoveDatastore", beta=True)
    @property
    def enable_site_to_move_datastore(self) -> Optional[bool]:
        """Gets the EnableSiteToMoveDatastore property"""
        return self.properties.get("EnableSiteToMoveDatastore", None)

    @odata(name="SourceCompanyId", beta=True)
    @property
    def source_company_id(self) -> Optional[UUID]:
        """Gets the SourceCompanyId property"""
        return self.properties.get("SourceCompanyId", None)

    @odata(name="SourceInstanceId", beta=True)
    @property
    def source_instance_id(self) -> Optional[UUID]:
        """Gets the SourceInstanceId property"""
        return self.properties.get("SourceInstanceId", None)

    @odata(name="SourceMySiteHostUrl", beta=True)
    @property
    def source_my_site_host_url(self) -> Optional[str]:
        """Gets the SourceMySiteHostUrl property"""
        return self.properties.get("SourceMySiteHostUrl", None)

    @odata(name="SourceSiteSubscriptionId", beta=True)
    @property
    def source_site_subscription_id(self) -> Optional[UUID]:
        """Gets the SourceSiteSubscriptionId property"""
        return self.properties.get("SourceSiteSubscriptionId", None)

    @odata(name="SourceSiteUrl")
    @property
    def source_site_url(self) -> Optional[str]:
        """Gets the SourceSiteUrl property"""
        return self.properties.get("SourceSiteUrl", None)

    @odata(name="TargetCompanyId", beta=True)
    @property
    def target_company_id(self) -> Optional[UUID]:
        """Gets the TargetCompanyId property"""
        return self.properties.get("TargetCompanyId", None)

    @odata(name="TargetFarmId", beta=True)
    @property
    def target_farm_id(self) -> Optional[str]:
        """Gets the TargetFarmId property"""
        return self.properties.get("TargetFarmId", None)

    @odata(name="TargetInstanceId", beta=True)
    @property
    def target_instance_id(self) -> Optional[UUID]:
        """Gets the TargetInstanceId property"""
        return self.properties.get("TargetInstanceId", None)

    @odata(name="TargetSiteSubscriptionId", beta=True)
    @property
    def target_site_subscription_id(self) -> Optional[UUID]:
        """Gets the TargetSiteSubscriptionId property"""
        return self.properties.get("TargetSiteSubscriptionId", None)

    @odata(name="TargetSiteUrl")
    @property
    def target_site_url(self) -> Optional[str]:
        """Gets the TargetSiteUrl property"""
        return self.properties.get("TargetSiteUrl", None)

    @odata(name="TenantMergeSourceMySiteHostUrl", beta=True)
    @property
    def tenant_merge_source_my_site_host_url(self) -> Optional[str]:
        """Gets the TenantMergeSourceMySiteHostUrl property"""
        return self.properties.get("TenantMergeSourceMySiteHostUrl", None)

    @odata(name="TenantMergeTargetMySiteHostUrl", beta=True)
    @property
    def tenant_merge_target_my_site_host_url(self) -> Optional[str]:
        """Gets the TenantMergeTargetMySiteHostUrl property"""
        return self.properties.get("TenantMergeTargetMySiteHostUrl", None)
