Feature: Repository management
  As a user
  I want to clone, list, and switch repositories via the API
  So that I can manage multiple git repositories from a single backend

  Scenario: Clone a new repository
    Given the API is running
  When I POST to /users/alice/repos with name "git-rest-test" and url "https://github.com/jondavid-black/git-rest-test.git"
    Then the response status should be 201
  And the response should contain "name": "git-rest-test"

  Scenario: List repositories
    Given the API is running
    When I GET /users/alice/repos
    Then the response status should be 200
    And the response should be a list

  Scenario: Get repository details
    Given the API is running
  And a repository named "git-rest-test" exists
  When I GET /users/alice/repos/git-rest-test
  Then the response status should be 200
  And the response should contain "name": "git-rest-test"

  Scenario: Switch active repository
    Given the API is running
  And a repository named "git-rest-test" exists
  When I POST to /users/alice/repos/git-rest-test
  Then the response status should be 200
  And the response should contain "message": "Switched to repository 'git-rest-test'"
