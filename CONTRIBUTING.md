# Welcome Contributors! 🎉

Thank you for your interest in contributing to the Office365-REST-Python-Client library. This project provides a comprehensive Python client for Microsoft 365 and Microsoft Graph APIs.

## Table of Contents

1. Getting Started
2. Development Environment Setup
3. Code Style and Quality Standards
4. Testing Guidelines
5. Submitting Changes
6. Issue Reporting
7. Documentation
8. Community Guidelines

## Getting Started

### Prerequisites

- Python 3.6+
- Git
- A Microsoft 365 tenant for testing (recommended)
- Basic understanding of REST APIs and Microsoft Graph/SharePoint APIs

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/your-username/Office365-REST-Python-Client.git
cd Office365-REST-Python-Client
```

## Development Environment Setup

Activate the Virtual Environment and install dependencies:

```bash
uv sync --all-extras
```

### Pre-commit hooks (recommended)

```bash
uv tool install prek
prek run --all-files
```

## Code Style and Quality Standards

The project uses the following tools (mirroring CI):

- Black (formatting)
- Ruff (linting and import sorting)
- Pylint (static analysis)

Line length: 121 characters (configured in `pyproject.toml`).

Run locally before pushing:

```bash
prek
```

## Testing Guidelines

Most tests are end-to-end and require actual Microsoft 365 credentials.

### Test Configuration

1. Create a `.env` file in the project root:

   ```bash
   export office365_python_sdk_securevars='{username};{password};{client_id};{client_secret}'
   ```

2. Source the environment file:

   ```bash
   . .env
   ```

Note: The order of values is significant because tests parse by index.

### Required Tenant Permissions

For comprehensive testing, your test tenant should have these admin roles:

- Global reader
- Groups admin
- Search admin
- SharePoint admin
- Teams service admin

### Running Tests

```bash
pytest
# or
pytest -v
# or a specific suite
pytest tests/sharepoint/
```

CI note: Full E2E tests in CI rely on repository secrets and may not run on forks. Please run tests locally; maintainers trigger full CI runs as needed.

### Forks and CI

- Forked pull requests do not receive repository secrets. The CI pipeline will run formatting and linting, and it will skip `pytest` automatically if secrets are unavailable.
- To validate your changes, run tests locally using your own tenant credentials as described above.
- Maintainers will run the full E2E test suite on branches with access to secrets before merging.

## Submitting Changes

### Branching Strategy

1. Create a feature branch from `master`:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes with clear, focused commits
3. Ensure all tests pass and quality checks are satisfied

### Pull Request Process

1. CI Checks must pass:
   - Ruff linting
   - Black formatting
   - Pylint analysis
   - Pytest execution
2. Await maintainer review
3. Update documentation where applicable

### Commit Guidelines

- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Keep commits focused and atomic

## Issue Reporting

Before filing an issue:

1. Search existing issues
2. Check documentation and examples
3. Test with the latest version

Include in your report:

- Environment: Python version, OS, library version
- Reproduction: minimal code example
- Expected vs Actual behavior
- Authentication method used
- Targeted service area (SharePoint, Graph, etc.)

## Documentation

### API Coverage

The library supports multiple Microsoft 365 APIs, including SharePoint REST, Microsoft Graph, OneDrive, Outlook, Teams, OneNote, and Planner. See `examples/` for usage.

## Community Guidelines

This project is maintained by the community. Be respectful and constructive in all interactions.

### License

MIT License. By contributing, you agree that your contributions are licensed under these terms.
