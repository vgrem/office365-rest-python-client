"""A generated function submits the URL its CSDL names - measured on the service.

The generator is the only thing that writes these methods, and its failure mode is a wire
shape: a function whose parameters are listed instead of named is read as a navigation
property, and a function whose parameters are omitted needs no parentheses at all. Neither
is visible to an in-process assertion, so this file talks to the tenant.

What it deliberately does *not* assert:

  * the contents. An empty collection and a calendar holding no reminders are both correct
    answers, so an item assertion would fail on a quiet tenant rather than on a defect.
  * the 638 generated *actions*. A bound action submits a POST body, so proving one needs a
    write scope and a disposable object; the action shape is pinned offline in
    ``tests/tooling/test_generator_e2e.py`` and has not been measured here.
"""

from __future__ import annotations

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase


class TestAFunctionIsAddressedByNamedParameters(GraphDelegatedTestCase):
    """``GET .../reminderView(startDateTime='...',endDateTime='...')``.

    Positional values produced 400 "Open navigation properties are not supported on
    OpenTypes. Property name: 'reminderView'" - Graph read the call as a property access.
    """

    def test_01_now_is_a_reminder_view(self):
        """Two named parameters, a collection of client values back.

        Declares no scope: the tenant that proved this holds the legacy ``.All`` grants, whose
        names Microsoft Graph does not publish for the delegated flow, so a declared scope
        would skip the test in the one tenant where it has been measured. A refusal is a skip
        with the service's own words; anything else a call can get wrong is a failure.
        """
        start, end = "2026-01-01T00:00:00Z", "2027-01-01T00:00:00Z"
        try:
            result = self.client.me.reminder_view(start, end).execute_query()
        except ClientRequestException as error:
            self.skipTest(f"the tenant refused the call: {error}")

        self.assertIsInstance(result.value, ClientValueCollection)
        items = list(result.value)
        if items:
            self.assertEqual("microsoft.graph.Reminder", items[0].entity_type_name)

    def test_02_the_wire_order_is_the_csdl_order(self):
        """The path builder renders ``name(param=value,...)`` and nothing else.

        Read off the query's own URL rather than a hand-built string: the point is what the
        library sends, and this is the only place that can see it without a transport fake.
        """
        start, end = "2026-01-01T00:00:00Z", "2027-01-01T00:00:00Z"
        query = FunctionQuery(self.client.me, "reminderView", {"startDateTime": start, "endDateTime": end}, None)

        self.assertTrue(
            query.url.endswith(f"/reminderView(startDateTime='{start}',endDateTime='{end}')"),
            query.url,
        )


class TestAFunctionWithNoParametersOmitsTheParentheses(GraphApplicationTestCase):
    """``GET /reports/getOffice365ActivationsUserDetail`` - accepted without ``()``."""

    @requires_application("Reports.Read.All")
    def test_01_no_parameters(self):
        """The declared ``Report`` type carries the payload as bytes."""
        result = self.client.reports.get_office365_activations_user_detail().execute_query()

        content = result.value.to_bytes()
        self.assertTrue(content, "a report with no content is not an empty report")
        self.assertIn(b"Report Refresh Date", content)


class TestAFunctionWithOneParameter(GraphApplicationTestCase):
    """``GET /reports/getOffice365ActiveUserDetail(period='D7')``."""

    @requires_application("Reports.Read.All")
    def test_01_one_parameter(self):
        """A single named parameter reaches the service and comes back as a CSV."""
        result = self.client.reports.get_office365_active_user_detail("D7").execute_query()

        content = result.value.to_bytes()
        self.assertIn(b"User Principal Name", content)
