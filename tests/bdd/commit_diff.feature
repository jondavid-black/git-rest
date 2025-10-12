Feature: Commit and diff operations
  As a user
  I want to commit changes and view diffs via the API
  So that I can manage file changes in my repositories

  Background:
    Given the API is running
  And a repository named "git-rest-test" exists

  Scenario: Commit changes
  When I POST to /users/alice/repos/git-rest-test/commit with message "Initial commit" and author "Alice"
    Then the response status should be 201
    And the response should contain "message": "Initial commit"

  Scenario: Get working tree diff
  When I GET /users/alice/repos/git-rest-test/diff
    Then the response status should be 200
    And the response should contain "diff"

  Scenario: Get diff between two commits
  Given two commits exist in "users/alice/git-rest-test"
  When I GET /users/alice/repos/git-rest-test/diff?a={commit_a}&b={commit_b}
    Then the response status should be 200
    And the response should contain "diff"

  Scenario: Commit to git-rest-test-other and verify isolation
    Given the API is running
    And a repository named "git-rest-test-other" exists
    When I POST to /users/alice/repos/git-rest-test-other/commit with message "Other commit" and author "Alice"
    Then the response status should be 201
    And the response should contain "message": "Other commit"
    When I GET /users/alice/repos/git-rest-test/diff
    Then the response should not contain "Other commit"

  Scenario: Commit to git-rest-test and verify isolation
    Given the API is running
    And a repository named "git-rest-test" exists
    When I POST to /users/alice/repos/git-rest-test/commit with message "Test commit" and author "Alice"
    Then the response status should be 201
    And the response should contain "message": "Test commit"


  # --- Edge Case Scenario ---

  Scenario: Commit in detached HEAD state
    Given the API is running
    And a repository named "git-rest-test" exists
    # Simulate detached HEAD by creating a commit, then checking out a commit hash
    When I POST to /users/alice/repos/git-rest-test/commit with message "Initial commit" and author "Alice"
    Then the response status should be 201
    And the response should contain "message": "Initial commit"
    When I detach HEAD in repo "git-rest-test"
    When I POST to /users/alice/repos/git-rest-test/commit with message "Detached commit" and author "Alice"
    Then the response status should be 400
    And the response should contain "error": "Cannot commit in detached HEAD state."
    When I GET /users/alice/repos/git-rest-test-other/diff
    Then the response should not contain "Test commit"
