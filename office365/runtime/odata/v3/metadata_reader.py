from typing import Dict

from office365.runtime.odata.reader import ODataReader


class ODataV3Reader(ODataReader):
    """OData v3 reader"""

    @property
    def xml_namespaces(self) -> Dict[str, str]:
        return {
            "xmlns": "http://schemas.microsoft.com/ado/2009/11/edm",
            "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
            "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
        }
