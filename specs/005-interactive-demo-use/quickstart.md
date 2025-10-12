# Quickstart: Interactive Demo - Use flasgger

## Prerequisites
- Python 3.12+
- Flask
- flasgger
- pytest, Behave (for testing)

## Setup
1. Install dependencies:
   ```bash
   pip install flask flasgger pytest behave
   ```
2. Set the environment variable to enable the interactive demo UI:
   ```bash
   export ENABLE_INTERACTIVE_DEMO=1
   # The demo UI will be available at /apidocs
   ```
3. Run the Flask app:
   ```bash
   flask run
   ```
4. Access the interactive demo UI at `/apidocs` in your browser.

## Disabling the Demo
- To disable the demo UI, unset or set the environment variable to `0`:
   ```bash
   export ENABLE_INTERACTIVE_DEMO=0
   # The demo UI will not be available
   ```

## Adding/Updating Endpoints
- Add or update Flask blueprints/routes as usual. The demo UI will update automatically on app restart.

## Testing
- Run unit and acceptance tests:
  ```bash
  pytest
  behave
  ```

## Notes
- The demo UI requires no manual updates as the API evolves.
- Each endpoint should have a docstring for best documentation results.
