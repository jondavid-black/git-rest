# Data Model: Exception Exposure - Secure Error Responses

## Entities

### Error Response
- Fields:
  - message: string
  - code: string
  - timestamp: datetime

### Error Log Entry
- Fields:
  - exception_type: string
  - stack_trace: string
  - timestamp: datetime
  - request_context: object
  - user_data: object (may include user data per clarification)

## Relationships
- Error Response is generated from Error Log Entry
- Error Log Entry may reference a user (if applicable)

## Validation Rules
- Error Response must not include raw exception content or stack traces
- Error Log Entry may include user data and is accessible to all developers
- All fields required except user_data (optional)

## State Transitions
- Error occurs → Error Log Entry created
- Error Log Entry processed → Error Response generated for user
