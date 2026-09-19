# Roadmap

Public roadmap for `office365-rest-python-client`.

Funding (via [GitHub Sponsors](https://github.com/sponsors/vgrem), Open Collective, or
custom engagements) directly supports the items below. Community contributions are welcome too.

## Near term

- [ ] **Dependency and security upkeep** — keep `cryptography`, MSAL, and `requests` current
      and respond to CVEs quickly (the library has shipped several security-driven releases).
- [ ] **Issue backlog** — triage and fix the open issue queue.
- [ ] **Type-hint completion** — finish static type coverage across the remaining modules.

## Mid term

- [ ] **Graph API coverage** — expand Planner, Intune, and Teams admin surface area.
- [ ] **SharePoint Online auth docs** — clear guidance for app-only, certificate, and
      ROPC flows (post-ACS-retirement).
- [ ] **Schema sync** — keep the generator and metadata aligned with Microsoft's evolving
      Graph and SharePoint schemas.

## Ongoing

- [ ] Maintain the examples library (100+ runnable examples across SharePoint, Graph, Entra ID).
- [ ] Monthly release cadence with changelog entries.
- [ ] Responsive issue support and community review of PRs.

## Funding this work

Sponsorship is entirely optional — the library stays free and MIT-licensed, and it
never affects whether an issue is fixed.

- **Individuals:** [GitHub Sponsors](https://github.com/sponsors/vgrem), [Ko-fi](https://ko-fi.com/vgrem), or [PayPal](https://paypal.me/ossvgrem).
- **Companies:** invoiced sponsorship or a custom paid support / feature engagement
  — see the Support section of the README.
- **Contributing:** bug reports, PRs, and example scripts are all appreciated.

### How sponsorship is used

- Dependency and security upkeep (keeping MSAL, `cryptography` and `requests` current).
- Release engineering (releases, changelogs, PyPI and docs publishing).
- Issue triage and community review of pull requests.
- New API coverage, examples, and documentation.
