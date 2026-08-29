"""
Generate a documentation page per example script (mkdocs-gen-files plugin).

For every script under ``MKDOCS_EXAMPLES_ROOT`` (default ``examples``) emit
``examples/<rel>.md`` (module docstring as the narrative + full source).
Every directory that contains a ``README.md`` gets an index page
(``examples/<rel>/index.md``), so the gallery mirrors the product →
namespace layout (e.g. ``sharepoint/files/``, ``outlook/messages/``).
Relative ``.py``/``README.md`` links in those READMEs are rewritten to the
generated pages; the top-level ``examples/README.md`` becomes the gallery
landing page.

The navigation is derived from the generated pages by ``mkdocs-awesome-pages``,
so no nav file is needed here. To keep the sidebar compact, every subdirectory
gets a ``.pages`` that hides its per-example pages (only the directory index is
shown); the product root gets a ``.pages`` with a pretty title and its
root-level scripts hidden behind the product index — all examples stay reachable
via the index pages.

Every example is parsed with ``ast`` and every README link is validated, so
``mkdocs build --strict`` fails on invalid Python or a README referencing a
missing file.

mkdocs-gen-files executes this module with ``runpy``, so emission must happen
at module level.
"""

from __future__ import annotations

import ast
import os
import pathlib
import re

import mkdocs_gen_files

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAMPLES_ROOT = pathlib.Path(os.environ.get("MKDOCS_EXAMPLES_ROOT", REPO_ROOT / "examples"))

_REL_LINK = re.compile(r"\]\(((?:\.\./|\./)?[^)#]+?)\)")

# Pretty sidebar titles for the product galleries (folder names are the fallback).
_PRODUCT_TITLES = {
    "admin": "Microsoft 365 Admin",
    "backuprestore": "Backup & Restore",
    "booking": "Microsoft Bookings",
    "communications": "Cloud Communications",
    "defender": "Microsoft Defender",
    "entraid": "Microsoft Entra ID",
    "insights": "Insights",
    "intune": "Microsoft Intune",
    "onedrive": "OneDrive",
    "onenote": "OneNote",
    "outlook": "Outlook",
    "planner": "Planner",
    "purview": "Microsoft Purview",
    "reports": "Usage Reports",
    "security": "Security",
    "sharepoint": "SharePoint",
    "teams": "Microsoft Teams",
    "todo": "Microsoft To Do",
}


def _emit(path: str, content: str) -> None:
    with mkdocs_gen_files.open(path, "w") as f:
        f.write(content)


def _rewrite_links(text: str, base: pathlib.Path) -> str:
    """Rewrite relative links in a README to the generated pages.

    Script links (``.py`` or extensionless), ``README.md`` links, and directory
    links become the page's source file (e.g. ``foo.md`` / ``bar/index.md``);
    absolute links, anchors, and other ``.md`` links are left untouched.
    """

    def _sub(match: re.Match) -> str:
        rel = match.group(1)
        if rel.startswith(("http://", "https://", "mailto:", "#", "//")):
            return match.group(0)

        target = (base / rel).resolve()
        if not target.exists():
            candidate = (base / f"{rel}.py").resolve()
            if not candidate.exists():
                raise FileNotFoundError(f"README links to missing file: {target}")
            target = candidate

        if target.is_dir():
            if (target / "README.md").exists() or any(target.rglob("*.py")):
                page = target / "index.md"
            else:
                page = pathlib.Path(f"{target}.md")
                if not page.exists():
                    raise FileNotFoundError(f"README links to missing page: {page}")
        elif target.suffix == ".py":
            page = target.with_suffix(".md")
        elif target.name in ("README.md", "readme.md"):
            page = target.parent / "index.md"
        else:
            return match.group(0)

        return f"]({os.path.relpath(page, base)})"

    return _REL_LINK.sub(_sub, text)


def _emit_product(product: pathlib.Path) -> None:
    """Emit all pages for one top-level product area under docs/<product>/."""
    if not any(product.rglob("*.py")):
        return  # sample data / non-code directories
    prefix = "auth" if product.name == "auth" else f"products/{product.name}"

    for path in sorted(product.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8")), clean=False) or ""
        title = (doc.strip().splitlines() or [path.stem])[0].lstrip("# ").strip() or path.stem
        rel = path.relative_to(product).with_suffix(".md")
        _emit(f"{prefix}/{rel}", f"# {title}\n\n{doc}\n\n```python\n{path.read_text(encoding='utf-8')}\n```\n")

    for readme in sorted(product.rglob("README.md")):
        if "__pycache__" in readme.parts:
            continue
        rel = readme.parent.relative_to(product)
        key = f"{prefix}/{rel}/index.md" if rel.parts else f"{prefix}/index.md"
        _emit(key, _rewrite_links(readme.read_text(encoding="utf-8"), readme.parent))

    # hide the per-example pages under every subdirectory — the directory index links to them
    for directory in sorted({p.parent for p in product.rglob("*.py")}):
        if directory == product or directory.name.startswith("__"):
            continue
        rel = directory.relative_to(product)
        if not (directory / "README.md").exists():
            lines = [f"# {_section_title(directory)}", "", "Examples:"]
            for child in sorted(directory.iterdir()):
                if child.is_dir() and not child.name.startswith("__"):
                    lines.append(f"- [{child.name.replace('_', ' ').title()}]({child.name}/index.md)")
                elif child.suffix == ".py":
                    lines.append(f"- [{child.stem.replace('_', ' ').title()}]({child.stem}.md)")
            _emit(f"{prefix}/{rel}/index.md", "\n".join(lines) + "\n")
        _emit(f"{prefix}/{rel}/.pages", f"title: {_section_title(directory)}\nnav:\n  - index.md\n")

    # prettify the product section and hide root-level scripts behind the product index
    if product.name != "auth":
        title = _PRODUCT_TITLES.get(product.name, product.name.replace("_", " ").title())
        subdirs = sorted(
            d.name for d in product.iterdir() if d.is_dir() and not d.name.startswith("__") and any(d.rglob("*.py"))
        )
        nav = ["nav:", "  - index.md"] + [f"  - {name}" for name in subdirs]
        _emit(f"{prefix}/.pages", f"title: {title}\n" + "\n".join(nav) + "\n")


def _section_title(directory: pathlib.Path) -> str:
    """Sidebar title for a directory: its README heading, else the folder name."""
    readme = directory / "README.md"
    if readme.exists():
        match = re.search(r"^#\s+(.+)$", readme.read_text(encoding="utf-8"), re.M)
        if match:
            return re.sub(r"^Working with\s+", "", match.group(1).strip(), flags=re.I)
    return directory.name.replace("_", " ").title()


for product in sorted(p for p in EXAMPLES_ROOT.iterdir() if p.is_dir() and not p.name.startswith("__")):
    _emit_product(product)
