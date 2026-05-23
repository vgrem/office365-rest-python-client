# Site Designs & Site Scripts

Site designs bundle one or more site scripts into a packaged template
that can be applied to new or existing sites. Site scripts define the
actual JSON actions (theme, navigation, lists, etc.).

| What | File | Notes |
|------|------|-------|
| **Create design** | [`create_design.py`](./create_design.py) | Create a site script + bundle into a site design |
| **List designs** | [`list_designs.py`](./list_designs.py) | Enumerate all site designs |
| **Get design** | [`get_design.py`](./get_design.py) | Get metadata for a specific design |
| **Update design** | [`update_design.py`](./update_design.py) | Change title, description, or linked scripts |
| **Delete design** | [`delete_design.py`](./delete_design.py) | Remove a site design |
| **Design from web** | [`design_from_web.py`](./design_from_web.py) | Export a live site → script → design |
| **Apply design** | [`apply_design.py`](./apply_design.py) | Apply a design asynchronously to a site |
| **Grant rights** | [`grant_rights.py`](./grant_rights.py) | Grant/revoke principal access to a design |

## Site Scripts

| What | File | Notes |
|------|------|-------|
| **Create script** | [`../sitescripts/create.py`](../sitescripts/create.py) | Create a site script from JSON actions |
| **List scripts** | [`../sitescripts/list_scripts.py`](../sitescripts/list_scripts.py) | Enumerate all site scripts |
| **Delete script** | [`../sitescripts/delete_script.py`](../sitescripts/delete_script.py) | Remove a site script by ID |
| **From list** | [`../sitescripts/get_from_list.py`](../sitescripts/get_from_list.py) | Generate script from an existing list |
| **From web** | [`../sitescripts/get_from_web.py`](../sitescripts/get_from_web.py) | Generate script from an existing site |

---

## Official docs

- [Site design overview](https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview)
- [Site design JSON schema](https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-json-schema)
