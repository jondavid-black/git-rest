Feature: Repository management
  As a user
  I want to clone, list, and switch repositories via the API
  So that I can manage multiple git repositories from a single backend

  Scenario: Clone a new repository
    Given the API is running
    When I POST to /repos with name "sample-repo" and url "https://github.com/example/sample-repo.git"
    Then the response status should be 201
    And the response should contain "name": "sample-repo"

  Scenario: List repositories
    Given the API is running
    When I GET /repos
    Then the response status should be 200
    And the response should be a list

  Scenario: Get repository details
    Given the API is running
    And a repository named "sample-repo" exists
    When I GET /repos/sample-repo
    Then the response status should be 200
    And the response should contain "name": "sample-repo"

  Scenario: Switch active repository
    Given the API is running
    And a repository named "sample-repo" exists
    When I POST to /repos/sample-repo
    Then the response status should be 200
    And the response should contain "message": "Switched to repository 'sample-repo'"
