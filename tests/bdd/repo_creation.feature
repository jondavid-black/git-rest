Feature: Repository creation via API
  As a user
  I want to create a new repository with a name, description, README, and license
  So that I can start managing code with git-rest

  Scenario: Create a new repository with all fields
    Given the API server is running
    When I POST to /api/repos with name "bdd-repo", description "BDD repo", license "MIT", and README "# BDD Repo\nCreated by Behave"
    Then the response status code should be 201
    And the response should contain "name", "description", "license", and "readme"
    And a directory "test_working_dir/JD/bdd-repo" should exist
    And the files "README.md" and "LICENSE" should exist in that directory

  Scenario: Attempt to create a repository with a duplicate name
    Given the API server is running
    And a repository named "bdd-repo" already exists
    When I POST to /api/repos with name "bdd-repo"
    Then the response status code should be 400
    And the response should contain an error message about duplicate name

  Scenario: Create a repository with invalid license
    Given the API server is running
    When I POST to /api/repos with name "invalid-license-repo", description "Bad license", license "NOT_A_LICENSE"
    Then the response status code should be 400
    And the response should contain an error message about license

  Scenario: Create a repository with missing name
    Given the API server is running
    When I POST to /api/repos with name ""
    Then the response status code should be 400
    And the response should contain an error message about name
