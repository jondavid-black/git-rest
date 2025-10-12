# Quickstart: Multi-Repo Testing

## Prerequisites
- Python 3.12+
- All dependencies installed (see `pyproject.toml`)
- Behave and pytest installed

## Steps
1. Start the git-rest API server (see main docs for details)
2. Ensure test repos are accessible:
   - https://github.com/jondavid-black/git-rest-test
   - https://github.com/jondavid-black/git-rest-test-other
3. Run Behave BDD tests:
   ```bash
   cd tests
   behave bdd/
   ```
4. Review test results for multi-repo scenarios:
   - Cloning both repos
   - Switching between repos
   - Commit isolation
   - Origin verification
   - Error handling (e.g., name collision)

## Troubleshooting
- Ensure no repo name collisions in test environment
- Check logs for clear error messages if tests fail
- For performance issues, verify local disk speed and server load
