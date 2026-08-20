"""
Deep-inspect a content type: metadata, flags, field links, and schema XML.

The schema XML can be written to a file — useful for audit, backup, and
provisioning content types on other sites.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Inspect a content type and export its schema")
    parser.add_argument("--name", required=True, help="Content type name")
    parser.add_argument("--output", default=None, help="write schema XML to this file (otherwise print)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    ct = ctx.web.content_types.get_by_name(args.name)
    ctx.load(
        ct,
        [
            "Name",
            "Description",
            "Group",
            "StringId",
            "SchemaXml",
            "ReadOnly",
            "Sealed",
            "Hidden",
            "DocumentTemplateUrl",
            "Scope",
        ],
    ).execute_query()
    links = ct.field_links.get().execute_query()

    print(f"Name:               {ct.name}")
    print(f"Description:        {ct.description}")
    print(f"Group:              {ct.group}")
    print(f"StringId:           {ct.string_id}")
    print(f"Scope:              {ct.scope}")
    print(f"ReadOnly:           {ct.read_only}   Sealed: {ct.sealed}   Hidden: {ct.hidden}")
    print(f"DocumentTemplate:   {ct.document_template_url}")
    print(f"Field links ({len(links)}):")
    for link in links:
        flags = []
        if link.required:
            flags.append("required")
        if link.hidden:
            flags.append("hidden")
        if link.read_only:
            flags.append("read-only")
        print(f"  {link.field_internal_name:30s} {', '.join(flags) or '-'}")

    schema = ct.schema_xml or ""
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(schema)
        print(f"Schema XML written to {args.output}")
    else:
        print("\nSchema XML:")
        print(schema)


if __name__ == "__main__":
    main()
