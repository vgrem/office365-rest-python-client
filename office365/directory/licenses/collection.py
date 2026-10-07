from office365.directory.licenses.subscribed_sku import SubscribedSku
from office365.entity_collection import EntityCollection


class SubscribedSkuCollection(EntityCollection[SubscribedSku]):
    """Subscribed SKUs collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, SubscribedSku, resource_path)

    def find_by_part_number(self, sku_part_number: str, *, required: bool = False) -> SubscribedSku:
        """Look up a subscribed SKU by its ``skuPartNumber``.

        ``GET /subscribedSkus`` supports only ``$select`` (no ``$filter``), so
        the collection is fetched and matched client-side, case-insensitively.
        Deferred — run with ``execute_query()``; the returned SKU is left
        uninitialized when none matches (check
        :attr:`~office365.runtime.client_object.ClientObject.is_loaded`). Pass
        ``required=True`` to raise instead (or on an ambiguous match).

        Args:
            sku_part_number (str): The SKU part number, e.g. ``ENTERPRISEPACK``
            required (bool): Raise on a missing or ambiguous match when ``True``
        """
        wanted = sku_part_number.upper()
        return self._find_by_predicate(
            lambda s: (s.sku_part_number or "").upper() == wanted,
            f"skuPartNumber eq '{sku_part_number}'",
            required=required,
        )
