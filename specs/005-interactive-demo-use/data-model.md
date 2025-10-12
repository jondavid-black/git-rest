# Data Model: Interactive Demo - Use flasgger

## Entities

### API Endpoint
- **Attributes:**
  - path (string)
  - method (string)
  - description (string, optional)
  - parameters (list, optional)
  - responses (list, optional)

### Interactive Demo UI
- **Attributes:**
  - endpoints (list of API Endpoint)
  - enabled (bool, from environment variable)

## Relationships
- The Interactive Demo UI displays all API Endpoints defined in the Flask app.
- Each API Endpoint may have zero or more parameters and responses.

## Validation Rules
- If an endpoint has no description, display a default message (e.g., "No documentation available.")
- The demo UI is only accessible if enabled by environment variable.

## State Transitions
- When a new route is added to the Flask app and the app is restarted, the new endpoint appears in the demo UI automatically.
