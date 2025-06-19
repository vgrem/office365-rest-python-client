from datetime import datetime

from office365.entity_collection import EntityCollection
from office365.onedrive.analytics.item_activity_stat import ItemActivityStat
from office365.runtime.queries.function import FunctionQuery


def build_get_activities_by_interval_query(
    binding_type,
    start_dt: datetime = None,
    end_dt: datetime = None,
    interval: str = None,
) -> FunctionQuery:
    """
    :param Entity binding_type: Binding type
    :param datetime start_dt: The start time over which to aggregate activities.
    :param datetime end_dt: The end time over which to aggregate activities.
    :param str interval: The aggregation interval.
    """
    params = {
        "startDateTime": start_dt.strftime("%m-%d-%Y") if start_dt else None,
        "endDateTime": end_dt.strftime("%m-%d-%Y") if end_dt else None,
        "interval": interval,
    }
    return_type = EntityCollection(
        binding_type.context, ItemActivityStat, binding_type.resource_path
    )
    qry = FunctionQuery(binding_type, "getActivitiesByInterval", params, return_type)
    return qry
