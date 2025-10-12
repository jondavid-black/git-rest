Feature: File delivery
  As a user
  I want to retrieve file listings and contents via the API
  So that I can access files in my repositories

  Background:
    Given the API is running
  And a repository named "git-rest-test" exists

  Scenario: List files in repository
  When I GET /users/alice/repos/git-rest-test/files
    Then the response status should be 200
    And the response should be a list

  Scenario: Retrieve small file content
  When I GET /users/alice/repos/git-rest-test/files/README.md
    Then the response status should be 200
    And the response should contain file content

  Scenario: Retrieve large file (redirect)
  Given a large file named "bigfile.bin" exists in "users/alice/git-rest-test"
  When I GET /users/alice/repos/git-rest-test/files/bigfile.bin
    Then the response status should be 302
    And the response should contain "url"

  Scenario: Download file via secure URL
  Given a secure URL for "bigfile.bin" in "users/alice/git-rest-test"
    When I GET the secure URL
    Then the response status should be 200
    And the response should contain file content
