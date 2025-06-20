from typing import List

from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.odata.query_options import QueryOptions


class QueryOptionsBuilder:
    """Builder for constructing QueryOptions instances."""

    @staticmethod
    def build(
        client_object: ClientObject, properties_to_include: List[str] = None
    ) -> QueryOptions:
        """Builds optimized query options for the given client object.

        Args:
            client_object: The target client object or collection
            properties_to_include: Properties to include in $select/$expand

        Returns:
            Configured QueryOptions instance
        """
        query_options = client_object.query_options
        if properties_to_include is None:
            return query_options

        for name in properties_to_include:
            if name in query_options.select:
                continue

            if isinstance(client_object, ClientObjectCollection):
                prop = client_object.create_typed_object().get_property(name)
            else:
                prop = client_object.get_property(name)

            if name == "Properties" or isinstance(prop, ClientObject):
                query_options.expand.append(name)
            query_options.select.append(name)
        return query_options
