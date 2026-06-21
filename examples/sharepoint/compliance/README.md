# SharePoint Compliance Tags (CSOM)

Examples for managing compliance tags (retention labels) on
SharePoint lists and items via the SharePoint CSOM API.

---

## Prerequisites

| Permission | Description |
|---|---|
| `Sites.Read.All` | Read lists and compliance tags |
| `Sites.ReadWrite.All` | Apply compliance tags |
| `Sites.FullControl.All` | Apply tags with hold, clear tags |

---

## Examples

| Scenario | File |
|---|---|
| List tags, get/applied tags, set tag with hold | [`retention_labels.py`](./retention_labels.py) |
| Report compliance tags across all lists | [`tag_report.py`](./tag_report.py) |
| Apply a compliance tag to a list | [`add_tag.py`](./add_tag.py) |
| Clear compliance tag from a list | [`remove_tag.py`](./remove_tag.py) |

---

## Important: compliance tags vs retention labels

Compliance tags in SharePoint CSOM (`get_available_tags()`) are **retention labels**
created in Microsoft Purview. Creating a label via the Graph API (see
`examples/purview/records/retention_label.py`) does **not** automatically make it
available in SharePoint — it must also be **published** via a **label policy**.

### Label policy vs Retention policy

| Type | What it does | Needed here? |
|------|-------------|-------------|
| **Label policy** | Publishes existing labels to locations so they can be **manually applied** to items | ✅ Yes — makes labels appear in `get_available_tags()` |
| **Retention policy** | Applies retention rules **automatically** to all content (no label visible) | ❌ No |

---

## How to publish a retention label to SharePoint

### Step 1: Create the label

Create the label either via the Graph API:

```bash
uv run examples/purview/records/retention_label.py
```

Or in the Purview portal: go to Solutions → Data Lifecycle Management →
Retention labels → Create a label.

### Step 2: Publish via a label policy

1. Go to [purview.microsoft.com](https://purview.microsoft.com)
2. Navigate to **Solutions** → **Data Lifecycle Management** → **Label policies**
3. Click **Create a label policy**
4. Choose **"Publish labels"**
5. **Select the labels** you want to make available in SharePoint
6. **Policy scope**: **Full directory** (or your specific admin unit)
7. **Locations**: Set **SharePoint sites** to **All sites** (or choose specific sites)
   — you can also enable Exchange, OneDrive, and Groups if desired
8. **Name your policy** (e.g. "Publish all labels — test")
9. Complete the wizard

### Step 3: Wait for sync

The policy takes **5-10 minutes** to sync. After that, the labels appear in
SharePoint's `get_available_tags()`.

### Step 4: Verify

Run the tag report to confirm:

```bash
uv run examples/sharepoint/compliance/tag_report.py
```

If your labels appear in the output, they are ready to be applied to lists
and items using the CSOM examples above.

---

## Applying labels via SharePoint CSOM

Once published, you can use the CSOM examples:

```bash
# Apply a label to the "Documents" list
uv run examples/sharepoint/compliance/add_tag.py

# Get a report of which lists have which labels
uv run examples/sharepoint/compliance/tag_report.py

# Clear a label from a list
uv run examples/sharepoint/compliance/remove_tag.py
```

---

## Official docs

- [SharePoint compliance tag REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/compliance/compliance-tag-rest-api)
- [Create retention labels via Graph API](../../purview/records/)
