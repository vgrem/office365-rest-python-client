import json
import os
import logging
import re

logger = logging.getLogger(__name__)

_VALID_REGION_RE = re.compile(r"^[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?$")

# IMDS compute metadata API version used for region auto-discovery.
# Bump this single constant when moving to a newer IMDS API version.
_IMDS_API_VERSION = "2021-02-01"


def _validate_region(region, source="unknown"):
    """Return *region* unchanged if it looks like a valid Azure region name,
    otherwise log a warning and return ``None``."""
    if region and _VALID_REGION_RE.fullmatch(region):
        return region
    if region:
        logger.warning(
            "Region from %s was discarded because it contains "
            "invalid characters: %r", source, region)
    return None


def _detect_region(http_client=None):
    region = os.environ.get("REGION_NAME", "")  # e.g. westus2
    if region:
        return _validate_region(region, source="REGION_NAME env variable")
    if http_client:
        return _detect_region_of_azure_vm(http_client)  # It could hang for minutes
    return None


def _detect_region_of_azure_vm(http_client):
    url = (
        "http://169.254.169.254/metadata/instance/compute"

        # The region is read from the "location" field of the compute metadata.
        # https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux#response-1
        "?api-version=" + _IMDS_API_VERSION
        )
    logger.info(
        "Connecting to IMDS {}. "
        "It may take a while if you are running outside of Azure. "
        "You should consider opting in/out region behavior on-demand, "
        'by loading a boolean flag "is_deployed_in_azure" '
        'from your per-deployment config and then do '
        '"app = ConfidentialClientApplication(..., '
        'azure_region=is_deployed_in_azure)"'.format(url))
    try:
        # https://docs.microsoft.com/en-us/azure/virtual-machines/windows/instance-metadata-service?tabs=linux#instance-metadata
        resp = http_client.get(url, headers={"Metadata": "true"})
    except:
        logger.info(
            "IMDS {} unavailable. Perhaps not running in Azure VM?".format(url))
        return None
    else:
        try:
            location = json.loads(resp.text).get("location")
        except (ValueError, AttributeError, TypeError):
            # ValueError: body is not valid JSON;
            # AttributeError: body is valid JSON but not a JSON object;
            # TypeError: resp.text is not a string (e.g. a custom http_client).
            logger.info("IMDS {} returned a malformed response.".format(url))
            return None
        if location is not None and not isinstance(location, str):
            logger.info("IMDS {} returned a non-string location.".format(url))
            return None
        return _validate_region(location, source="IMDS endpoint")
