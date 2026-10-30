from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class SharePointMigrationJobProgressEvent(Entity):
    @odata(name="bytesProcessed")
    @property
    def bytes_processed(self) -> Optional[int]:
        """Gets the bytesProcessed property"""
        return self.properties.get("bytesProcessed", None)

    @odata(name="bytesProcessedOnlyCurrentVersion")
    @property
    def bytes_processed_only_current_version(self) -> Optional[int]:
        """Gets the bytesProcessedOnlyCurrentVersion property"""
        return self.properties.get("bytesProcessedOnlyCurrentVersion", None)

    @odata(name="cpuDurationMs")
    @property
    def cpu_duration_ms(self) -> Optional[int]:
        """Gets the cpuDurationMs property"""
        return self.properties.get("cpuDurationMs", None)

    @odata(name="filesProcessed")
    @property
    def files_processed(self) -> Optional[int]:
        """Gets the filesProcessed property"""
        return self.properties.get("filesProcessed", None)

    @odata(name="filesProcessedOnlyCurrentVersion")
    @property
    def files_processed_only_current_version(self) -> Optional[int]:
        """Gets the filesProcessedOnlyCurrentVersion property"""
        return self.properties.get("filesProcessedOnlyCurrentVersion", None)

    @odata(name="isCompleted")
    @property
    def is_completed(self) -> Optional[bool]:
        """Gets the isCompleted property"""
        return self.properties.get("isCompleted", None)

    @odata(name="lastProcessedObjectId")
    @property
    def last_processed_object_id(self) -> Optional[str]:
        """Gets the lastProcessedObjectId property"""
        return self.properties.get("lastProcessedObjectId", None)

    @odata(name="objectsProcessed")
    @property
    def objects_processed(self) -> Optional[int]:
        """Gets the objectsProcessed property"""
        return self.properties.get("objectsProcessed", None)

    @odata(name="sqlDurationMs")
    @property
    def sql_duration_ms(self) -> Optional[int]:
        """Gets the sqlDurationMs property"""
        return self.properties.get("sqlDurationMs", None)

    @odata(name="sqlQueryCount")
    @property
    def sql_query_count(self) -> Optional[int]:
        """Gets the sqlQueryCount property"""
        return self.properties.get("sqlQueryCount", None)

    @odata(name="totalDurationMs")
    @property
    def total_duration_ms(self) -> Optional[int]:
        """Gets the totalDurationMs property"""
        return self.properties.get("totalDurationMs", None)

    @odata(name="totalErrors")
    @property
    def total_errors(self) -> Optional[int]:
        """Gets the totalErrors property"""
        return self.properties.get("totalErrors", None)

    @odata(name="totalExpectedBytes")
    @property
    def total_expected_bytes(self) -> Optional[int]:
        """Gets the totalExpectedBytes property"""
        return self.properties.get("totalExpectedBytes", None)

    @odata(name="totalExpectedObjects")
    @property
    def total_expected_objects(self) -> Optional[int]:
        """Gets the totalExpectedObjects property"""
        return self.properties.get("totalExpectedObjects", None)

    @odata(name="totalRetryCount")
    @property
    def total_retry_count(self) -> Optional[int]:
        """Gets the totalRetryCount property"""
        return self.properties.get("totalRetryCount", None)

    @odata(name="totalWarnings")
    @property
    def total_warnings(self) -> Optional[int]:
        """Gets the totalWarnings property"""
        return self.properties.get("totalWarnings", None)

    @odata(name="waitTimeOnSqlThrottlingMs")
    @property
    def wait_time_on_sql_throttling_ms(self) -> Optional[int]:
        """Gets the waitTimeOnSqlThrottlingMs property"""
        return self.properties.get("waitTimeOnSqlThrottlingMs", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJobProgressEvent"
