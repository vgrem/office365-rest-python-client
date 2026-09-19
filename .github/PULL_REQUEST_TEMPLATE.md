## Summary

<!-- What does this change do, and why? Link the related issue, e.g. "Fixes #123". -->

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation / examples
- [ ] Refactor / internal

## Checklist

<!-- Optional, but appreciated. Run the offline suite locally:
     uv sync --all-extras
     uv run ruff check . && uv run ruff format --check .
     uv run pyright
     uv run pytest --offline -q
-->

- [ ] `uv run ruff check .` and `uv run ruff format --check .` pass
- [ ] `uv run pyright` is clean
- [ ] `uv run pytest --offline -q` passes
- [ ] `uv run mkdocs build --strict` passes (if docs/examples changed)
- [ ] Added/updated tests under `tests/unit` where practical
- [ ] Linked the related issue
