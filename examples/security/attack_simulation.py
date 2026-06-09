"""
Attack simulation training — list phishing simulation campaigns,
automations, payloads, and training assignments.

Attack simulation is part of Microsoft 365 Defender. Security teams
use this to:
  - List active and past phishing simulations
  - View simulation automations (recurring campaigns)
  - Check landing pages configured for the tenant

Requires delegated permission ``AttackSimulation.Read.All`` and
``SecurityEvents.Read.All``.

https://learn.microsoft.com/en-us/graph/api/resources/attacksimulationroot
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    sim = client.security.attack_simulation

    # -- Step 1: list simulations (phishing campaigns) --
    simulations = sim.simulations.get().execute_query()
    print(f"Attack simulations: {len(simulations)}\n")

    for s in simulations:
        s_id = s.id or "?"
        display = s.properties.get("displayName", s.properties.get("name", "(unnamed)"))
        status = s.properties.get("status", "?")
        technique = s.properties.get("attackTechnique", "?")
        created = s.properties.get("createdDateTime", "?")
        if hasattr(created, "strftime"):
            created = created.strftime("%Y-%m-%d")

        completion = s.properties.get("completionDateTime", "?")
        if hasattr(completion, "strftime"):
            completion = completion.strftime("%Y-%m-%d")

        print(
            f"  {display:50s}  status={status:15s}  technique={technique:20s}  created={created}  complete={completion}"
        )

    # -- Step 2: list simulation automations (recurring campaigns) --
    automations = sim.simulation_automations.get().execute_query()
    print(f"\nSimulation automations: {len(automations)}")

    for a in automations:
        name = a.properties.get("displayName", "(unnamed)")
        status = a.properties.get("status", "?")
        print(f"  {name:50s}  status={status}")

        # Show automation runs
        runs = a.runs.get().execute_query()
        for r in runs:
            s_id = r.simulation_id or "?"
            run_status = r.properties.get("status", "?")
            run_dt = r.properties.get("startDateTime", "?")
            if hasattr(run_dt, "strftime"):
                run_dt = run_dt.strftime("%Y-%m-%d")
            print(f"    ↳ run: simulation={s_id[:20]}  status={run_status}  start={run_dt}")

    # -- Step 3: list landing pages --
    pages = sim.landing_pages.get().execute_query()
    print(f"\nLanding pages: {len(pages)}")
    for p in pages:
        lang = p.properties.get("locale", "?")
        status = p.properties.get("status", "?")
        print(f"  locale={lang:10s}  status={status}")


if __name__ == "__main__":
    main()
