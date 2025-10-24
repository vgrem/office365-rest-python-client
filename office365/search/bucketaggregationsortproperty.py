from enum import Enum


class BucketAggregationSortProperty(Enum):
    count = "0"
    keyAsString = "1"
    keyAsNumber = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BucketAggregationSortProperty"
