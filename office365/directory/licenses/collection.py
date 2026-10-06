from office365.directory.licenses.subscribed_sku import SubscribedSku
from office365.entity_collection import EntityCollection


class SubscribedSkuCollection(EntityCollection[SubscribedSku]):
    """Subscribed SKUs collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, SubscribedSku, resource_path)

    def get_by_part_number(self, sku_part_number: str) -> SubscribedSku:
        """Queue a lookup of a subscribed SKU by its ``skuPartNumber``.

        ``GET /subscribedSkus`` supports only ``$select`` (no ``$filter``), so
        the collection is fetched and matched client-side, case-insensitively.
        Deferred — run with ``execute_query()``; the returned SKU is left
        uninitialized when none matches (check
        :attr:`~office365.runtime.client_object.ClientObject.is_loaded`).

        Args:
            sku_part_number (str): The SKU part number, e.g. ``ENTERPRISEPACK``
        """
        return_type = self.create_typed_object()
        self.add_child(return_type)

        def _match(col: SubscribedSkuCollection) -> None:
            wanted = sku_part_number.upper()
            match = next((s for s in col if (s.sku_part_number or "").upper() == wanted), None)
            if match is None:
                return
            for k, v in match.properties.items():
                return_type.set_property(k, v, False)

        self.get().after_execute(_match)
        return return_type
