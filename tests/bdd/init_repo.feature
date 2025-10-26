Feature: Repository management

  Scenario: Initialize a new repository
    Given the API is running
  When I POST to the init endpoint for user "alice" with repo name "git-rest-init"
    Then the response status should be 201
    And the response should contain "url": "/users/alice/repos/git-rest-init"
    When I GET /users/alice/repos
    Then the response should be a list
    And the response should contain a repository named "git-rest-init"

  Scenario: Name collision when initializing repository
    Given the API is running
  When I POST to the init endpoint for user "alice" with repo name "git-rest-init"
    Then the response status should be 201
  When I POST to the init endpoint for user "alice" with repo name "git-rest-init"
    Then the response status should be 409
    And the response should contain "error": "Repository 'git-rest-init' already exists."

  Scenario: Invalid repository name when initializing
    Given the API is running
  When I POST to the init endpoint for user "alice" with repo name "invalid repo!"
    Then the response status should be 400
    And the response should contain "error"
