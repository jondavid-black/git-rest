Feature: File delivery
  As a user
  I want to retrieve file listings and contents via the API
  So that I can access files in my repositories

  Background:
    Given the API is running
    And a repository named "sample-repo" exists

  Scenario: List files in repository
    When I GET /repos/sample-repo/files
    Then the response status should be 200
    And the response should be a list

  Scenario: Retrieve small file content
    When I GET /repos/sample-repo/files/README.md
    Then the response status should be 200
    And the response should contain file content

  Scenario: Retrieve large file (redirect)
    Given a large file named "bigfile.bin" exists in "sample-repo"
    When I GET /repos/sample-repo/files/bigfile.bin
    Then the response status should be 302
    And the response should contain "url"

  Scenario: Download file via secure URL
    Given a secure URL for "bigfile.bin" in "sample-repo"
    When I GET the secure URL
    Then the response status should be 200
    And the response should contain file content
