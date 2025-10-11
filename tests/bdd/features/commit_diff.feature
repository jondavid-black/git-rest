Feature: Commit and diff operations
  As a user
  I want to commit changes and view diffs via the API
  So that I can manage file changes in my repositories

  Background:
    Given the API is running
    And a repository named "sample-repo" exists

  Scenario: Commit changes
    When I POST to /repos/sample-repo/commit with message "Initial commit" and author "Alice"
    Then the response status should be 201
    And the response should contain "message": "Initial commit"

  Scenario: Get working tree diff
    When I GET /repos/sample-repo/diff
    Then the response status should be 200
    And the response should contain "diff"

  Scenario: Get diff between two commits
    Given two commits exist in "sample-repo"
    When I GET /repos/sample-repo/diff?a={commit_a}&b={commit_b}
    Then the response status should be 200
    And the response should contain "diff"
