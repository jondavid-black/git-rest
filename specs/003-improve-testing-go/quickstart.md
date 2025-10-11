# Quickstart: Improve Testing

## Prerequisites
- Python 3.12+
- Install dependencies: `uv pip install -r requirements.txt`
- Ensure `pytest`, `behave`, `ruff`, and `coverage` are installed

## Running Unit Tests
1. From repo root, run:
   ```bash
   uv pip install -r requirements.txt
   pytest --cov=src/git_rest --cov-report=html
   ```
2. Open `htmlcov/index.html` to view coverage report
3. Ensure coverage is at least 75%

## Running BDD Acceptance Tests
1. From repo root, run:
   ```bash
   behave tests/bdd
   ```
2. All major workflows (clone, branch, commit, pull, merge, push, multi-repo/branch) should pass

## Adding New Tests
- Add unit tests to `tests/unit/`
- Add BDD scenarios to `tests/bdd/`
- Use mocks for external dependencies in unit tests

## CI/CD
- All tests and coverage checks are run automatically in GitHub Actions
- PRs must pass all tests and meet coverage requirements before merge

## Troubleshooting
- If coverage is below 75%, add more unit tests for uncovered functions
- For BDD failures, review step definitions and workflow logic
