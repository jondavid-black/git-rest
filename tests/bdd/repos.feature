Feature: Repository management


  Scenario: Switch repository performance is under 2 seconds
    Given the API is running
    And a repository named "git-rest-test" exists
    And a repository named "git-rest-test-other" exists
    When I measure the time to switch to repo "git-rest-test"
    Then the switch duration should be less than 2 seconds


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

  Scenario: Switch active repository to git-rest-test-other
    Given the API is running
    And a repository named "git-rest-test-other" exists
    When I POST to /users/alice/repos/git-rest-test-other
    Then the response status should be 200
    And the response should contain "message": "Switched to repository 'git-rest-test-other'"

  Scenario: Query origin for git-rest-test
    Given the API is running
    When I POST to /users/alice/repos with name "git-rest-test" and url "https://github.com/jondavid-black/git-rest-test.git"
    Then the response status should be 201
    When I GET /users/alice/repos/git-rest-test/origin
    Then the response status should be 200
    And the response should contain the correct origin for "git-rest-test"

  Scenario: Query origin for git-rest-test-other
    Given the API is running
    When I POST to /users/alice/repos with name "git-rest-test-other" and url "https://github.com/jondavid-black/git-rest-test-other.git"
    Then the response status should be 201
    When I GET /users/alice/repos/git-rest-test-other/origin
    Then the response status should be 200
    And the response should contain the correct origin for "git-rest-test-other"


  # --- Edge Case Scenarios ---

  Scenario: Name collision when cloning repository
    Given the API is running
    When I POST to /users/alice/repos with name "git-rest-test" and url "https://github.com/jondavid-black/git-rest-test.git"
    Then the response status should be 201
    When I POST to /users/alice/repos with name "git-rest-test" and url "https://github.com/jondavid-black/git-rest-test.git"
    Then the response status should be 400
    And the response should contain "error": "Repository 'git-rest-test' already exists."

  Scenario: Switch to non-existent repository
    Given the API is running
    When I POST to /users/alice/repos/nonexistent-repo
    Then the response status should be 404
    And the response should contain "error": "Repository 'nonexistent-repo' not found."

  Scenario: Network failure when cloning repository
    Given the API is running
    When I POST to /users/alice/repos with name "bad-remote" and url "https://invalid.example.com/nonexistent.git"
    Then the response status should be 400
    And the response should contain "error"
