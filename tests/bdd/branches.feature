Feature: Branch management
  As a user
  I want to list, create, switch, and delete branches via the API
  So that I can manage branches in my repositories

  Background:
    Given the API is running
  And a repository named "Hello-World" exists

  Scenario: List branches
  When I GET /repos/Hello-World/branches
    Then the response status should be 200
    And the response should be a list

  Scenario: Create a new branch
  When I POST to /repos/Hello-World/branches with name "feature-x"
    Then the response status should be 201
    And the response should be a list
  And the response should contain a branch named "feature-x"

  Scenario: Switch to a branch
  When I POST to /repos/Hello-World/branches/feature-x
    Then the response status should be 200
    And the response should contain "message": "Switched to branch 'feature-x'"

  Scenario: Delete a branch
  When I DELETE /repos/Hello-World/branches/feature-x
    Then the response status should be 200
    And the response should be a list
    And the response should not contain a branch named "feature-x"
