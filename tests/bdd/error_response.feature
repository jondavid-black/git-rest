Feature: Secure Error Responses
  As a user of the REST API
  I want error responses to be generic and not expose exception details
  So that sensitive server information is not leaked

  Scenario: Internal server error returns generic message
    When I request "/raise500"
    Then the response code should be 500
    And the response should contain "Internal server error"
    And the error response should not contain exception details

  Scenario: Unhandled exception returns generic message
    When I request "/raise_exception"
    Then the response code should be 500
    And the response should contain "Unexpected server error"
    And the error response should not contain exception details
