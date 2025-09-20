from typing import Dict

from office365.runtime.odata.reader import ODataReader


class ODataV4Reader(ODataReader):
    """OData v4 reader"""

    _options = None

    @property
    def xml_namespaces(self) -> Dict[str, str]:
        return {
            "xmlns": "http://docs.oasis-open.org/odata/ns/edm",
            "edmx": "http://docs.oasis-open.org/odata/ns/edmx",
        }
