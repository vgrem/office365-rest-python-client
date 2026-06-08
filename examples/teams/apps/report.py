"""
Report on apps installed across all Microsoft Teams.

Useful for detecting shadow IT — identifying apps installed without
admin approval, tracking legacy apps for retirement, and auditing
the app landscape across the tenant.

Inspired by Report-TeamsApps.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Team.ReadBasic.All              List all teams
    TeamsAppInstallation.Read.All   Read installed apps per team
    Directory.Read.All              (optional) read app catalog

https://learn.microsoft.com/en-us/graph/api/resources/teamsappinstallation
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def find_teams_apps() -> dict[str, list[dict]]:
    """Find all installed apps across teams.

    Returns:
        Dict mapping app name -> list of teams it's installed in.
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(
        test_client_id, test_client_secret
    )

    app_map = {}

    teams = client.teams.get_all().execute_query()
    for team in teams:
        team_id = team.id
        team_name = getattr(team, "display_name", "Unnamed")

        try:
            apps = client.teams[team_id].installed_apps.expand(["teamsAppDefinition"]).get().execute_query()
        except Exception:
            continue

        for app in apps:
            definition = getattr(app, "teams_app_definition", None) or getattr(app, "teamsAppDefinition", None)
            if not definition:
                continue

            app_name = getattr(definition, "display_name", "Unknown")
            app_version = getattr(definition, "version", "")
            app_publisher = getattr(definition, "publishing_state", "")

            if app_name not in app_map:
                app_map[app_name] = {
                    "version": app_version,
                    "publisher_state": app_publisher,
                    "teams": [],
                }
            app_map[app_name]["teams"].append(team_name)

    return app_map


def main():
    print("Scanning Teams apps across the tenant...\n")
    app_map = find_teams_apps()

    if not app_map:
        print("No installed apps found.")
        return

    # Sort by install count (most widespread first)
    sorted_apps = sorted(app_map.items(), key=lambda x: len(x[1]["teams"]), reverse=True)

    print(f"Found {len(sorted_apps)} distinct apps across {sum(len(v['teams']) for _, v in sorted_apps)} team installs\n")
    print(f"{'App':35s} {'Teams':>6s} {'Version':15s} {'State':10s}")
    print("-" * 70)
    for name, info in sorted_apps:
        abbreviation = "msft" if "microsoft" in name.lower() else "3rd"
        print(f"{name[:33]:35s} {len(info['teams']):>6d} {info['version'][:13]:15s} {info['publisher_state'][:8]:10s}")

    # Show least-widespread (potential shadow IT candidates)
    third_party = [(n, i) for n, i in sorted_apps if "microsoft" not in n.lower()]
    if third_party:
        print(f"\nThird-party apps ({len(third_party)}):")
        for name, info in third_party[:5]:
            print(f"  {name} — installed in {len(info['teams'])} team(s): {', '.join(info['teams'][:5])}")


if __name__ == "__main__":
    main()
