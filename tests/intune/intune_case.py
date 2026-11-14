"""Common ground for the Intune suites: the client pair, the scope families, and one guard.

An Intune test can fail to run for four different reasons, and they are not interchangeable:

* **the root.** ``self.dm`` is ``deviceManagement`` on the stable root and ``self.dm_beta``
  the same object on the preview root. Intune ships features on ``beta`` first - the script
  family, the Settings Catalog, assignment filters, the update profiles and intents have no
  ``v1.0`` counterpart at all - so a family the stable root refuses is read from
  ``self.dm_beta``, not skipped. Naming the object is how a suite says which root it means.
* **the permission.** The scope families below are grouped the way Intune groups them: a
  refusal names the whole set verbatim (*"Application must have one of the following scopes:
  ..."*), so these names are quotations, not paraphrases. ``@requires_delegated(*SCRIPTS)``
  is the test's precondition, and an ungranted set makes it skip naming the set - it never
  makes it pass.
* **the licence.** Licences are not a second permission here: measured, Intune answers with a
  scope list whether or not the caller holds Intune Plan 1 (the test tenant's user holds
  ``INTUNE_P2`` as provisioned while ``INTUNE_A`` sits at ``PendingInput``, and the Settings
  Catalog families answer ``200`` all the same). The published tables *do* tie one capability
  to an SKU - endpoint analytics needs Intune Plan 2 - and :data:`ENDPOINT_ANALYTICS` is that
  tie, used by ``test_endpoint_analytics.py`` and by nothing else.
* **the data.** An Intune object collection on a tenant nobody enrolled is empty, and an
  empty answer is a fact, not a failure. :meth:`IntuneCase.read` sends the read and
  :meth:`IntuneCase.row_or_skip` skips only when the service answered with nothing.

What is deliberately absent: ``bypass_roles``. The directory role does *not* satisfy the
service - measured on a caller holding Intune Administrator, ``deviceManagement/roleAssignments``
answers ``403`` naming ``DeviceManagementRBAC.Read.All`` - and ``except Exception: skipTest``,
which turns a ``403`` the declaration should have pinned, or a ``500`` worth reporting, into a
silent pass.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from tests.graph_case import GraphDelegatedTestCase

if TYPE_CHECKING:
    from office365.entity import Entity
    from office365.entity_collection import EntityCollection
    from office365.intune.devices.management.management import DeviceManagement

_EntityT = TypeVar("_EntityT", bound="Entity")

#: ``managedDevices``, ``detectedApps``, device categories, the per-device state lists.
#: Provenance: measured. A caller lacking them is told exactly this pair.
MANAGED_DEVICES = (
    "DeviceManagementManagedDevices.Read.All",
    "DeviceManagementManagedDevices.ReadWrite.All",
)

#: Device configurations, compliance policies, the Settings Catalog (``configurationPolicies``),
#: assignment filters, intents, update profiles. Provenance: measured for the families the
#: service refused; inferred for the ones it served to this app, which holds this pair and
#: not the ``Scripts``/``Apps``/``ServiceConfig``/``RBAC`` sets.
CONFIGURATION = (
    "DeviceManagementConfiguration.Read.All",
    "DeviceManagementConfiguration.ReadWrite.All",
)

#: The script family: ``deviceManagementScripts``, ``deviceShellScripts``,
#: ``deviceCustomAttributeShellScripts``, and by name ``deviceHealthScripts`` and
#: ``deviceComplianceScripts``, which refuse with a bare ``403`` naming nothing. Provenance:
#: measured for the first three, inferred for the last two.
SCRIPTS = (
    "DeviceManagementScripts.Read.All",
    "DeviceManagementScripts.ReadWrite.All",
)

#: ``mobileApps``, the app categories, app protection policies, ``auditEvents``, policy sets.
#: Provenance: measured.
APPS = (
    "DeviceManagementApps.Read.All",
    "DeviceManagementApps.ReadWrite.All",
)

#: Enrollment configuration, Autopilot profiles and identities, Terms and Conditions, the
#: management partners, mobile threat defence connectors. Provenance: measured - the refusal
#: also spells the same scope ``DeviceManagementServiceConfiguration`` (an Intune-only variant
#: Microsoft Graph does not publish), so only the published pair is declared here.
SERVICE_CONFIG = (
    "DeviceManagementServiceConfig.Read.All",
    "DeviceManagementServiceConfig.ReadWrite.All",
)

#: ``roleAssignments``, ``roleDefinitions``, ``roleScopeTags``. Provenance: measured.
RBAC = (
    "DeviceManagementRBAC.Read.All",
    "DeviceManagementRBAC.ReadWrite.All",
)

#: The only licence the published Intune tables turn into a capability: endpoint analytics is
#: Intune Plan 2 (which an E5 suite carries as the ``INTUNE_P2`` service plan). One name, so a
#: tenant that bought the Intune Suite under another plan name shows up as a skip to widen
#: here rather than as a silent pass.
ENDPOINT_ANALYTICS = ("INTUNE_P2",)


class IntuneCase(GraphDelegatedTestCase):
    """A live Intune suite: both service roots, and a guard for the data being absent."""

    @property
    def dm(self) -> DeviceManagement:
        """``deviceManagement`` on the stable service root."""
        return self.client.device_management

    @property
    def dm_beta(self) -> DeviceManagement:
        """The same object on the preview root, where most of Intune actually lives."""
        return self.client_beta.device_management

    def read(self, collection: EntityCollection[_EntityT], segment: str, limit: int = 5) -> EntityCollection[_EntityT]:
        """Assert the wire, send the read, and hand back the rows - which may be none.

        The path is checked before the request: a getter that built the wrong segment would
        otherwise pass on whatever the service happened to answer, and an assertion that never
        looks at the request is a test of the mock, not of the model.
        """
        self.assertTrue(
            str(collection.resource_path).endswith(f"/{segment}"),
            f"{collection.resource_path} does not address /{segment}",
        )
        return collection.top(limit).get().execute_query()

    def row_or_skip(self, rows: EntityCollection[_EntityT], what: str) -> _EntityT:
        """The first of ``rows``, or a skip saying this tenant holds no ``what``.

        Only an answer that *arrived* gets here, so a refusal propagates from
        :meth:`read`: a ``403`` is the declaration being wrong, not the tenant being empty.
        """
        if not len(rows):
            self.skipTest(f"this tenant holds no {what}")
        return rows[0]
