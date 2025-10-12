Feature: Branch management
  As a user
  I want to list, create, switch, and delete branches via the API
  So that I can manage branches in my repositories

  Background:
    Given the API is running
  And a repository named "git-rest-test" exists

  Scenario: List branches
  When I GET /users/alice/repos/git-rest-test/branches
    Then the response status should be 200
    And the response should be a list

  Scenario: Create a new branch
  When I POST to /users/alice/repos/git-rest-test/branches with name "feature-x"
    Then the response status should be 201
    And the response should be a list
  And the response should contain a branch named "feature-x"

  Scenario: Switch to a branch
  When I POST to /users/alice/repos/git-rest-test/branches/feature-x
    Then the response status should be 200
    And the response should contain "message": "Switched to branch 'feature-x'"

  Scenario: Delete a branch
  When I DELETE /users/alice/repos/git-rest-test/branches/feature-x
    Then the response status should be 200
    And the response should be a list
    And the response should not contain a branch named "feature-x"
