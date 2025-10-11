Feature: Repository management
  As a user
  I want to clone, list, and switch repositories via the API
  So that I can manage multiple git repositories from a single backend

  Scenario: Clone a new repository
    Given the API is running
    When I POST to /users/alice/repos with name "Hello-World" and url "https://github.com/octocat/Hello-World.git"
    Then the response status should be 201
  And the response should contain "name": "Hello-World"

  Scenario: List repositories
    Given the API is running
    When I GET /users/alice/repos
    Then the response status should be 200
    And the response should be a list

  Scenario: Get repository details
    Given the API is running
  And a repository named "Hello-World" exists
    When I GET /users/alice/repos/Hello-World
  Then the response status should be 200
  And the response should contain "name": "Hello-World"

  Scenario: Switch active repository
    Given the API is running
  And a repository named "Hello-World" exists
    When I POST to /users/alice/repos/Hello-World
  Then the response status should be 200
  And the response should contain "message": "Switched to repository 'Hello-World'"
