# ⚠️ Azure ACS Retirement in Microsoft 365: Important Notice

**Target Audience:** Developers and administrators using SharePoint Online, Project Online, or SharePoint Add-ins.

## Key Retirement Dates

Azure Access Control Services (ACS) will be completely retired for Microsoft 365. Mark these critical dates:

*   **📅 November 1, 2024:** Azure ACS stopped working for **new tenants**.
*   **📅 April 2, 2026:** Azure ACS will be fully retired and **stop working for all existing tenants** (including Government Clouds).

After April 2, 2026, it will be impossible to use Azure ACS for authentication with SharePoint Online.

## Why This Matters for Your Code

Azure ACS was primarily used for two scenarios in Microsoft 365. Both are affected:

1.  **Provider-Hosted SharePoint Add-ins:** These Add-ins themselves are also retired. You must migrate these solutions.
2.  **Granting App-Only Access:** Applications using ACS for app-only authentication to SharePoint Online need to transition.

> **For SharePoint Server On-Premises:** This retirement **does not** impact SharePoint Server on-premises hybrid scenarios. No action is required there.

## Recommended Actions

Follow these steps to prepare your code and tenant:

### 1. Assess Your Current Usage
Run the **Microsoft 365 Assessment tool** to scan your tenant. It generates a Power BI report to help you:
*   Identify all existing Azure ACS application principals.
*   See their permission scopes and which sites they can access.
*   Plan the transition to **Microsoft Entra ID**.

### 2. Migrate Your Applications
You must switch any application currently using Azure ACS to use **Microsoft Entra ID** for authentication and authorization.

*   **🔗 Migration Guidance:** [https://aka.ms/retirement/acs/guidance](https://aka.ms/retirement/acs/guidance)
*   **🔗 SharePoint Add-in Retirement Info:** [https://aka.ms/retirement/addins/support](https://aka.ms/retirement/addins/support)
