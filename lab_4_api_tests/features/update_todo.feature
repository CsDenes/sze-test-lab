Feature: Update a to-do item
  As a user of the API
  I want to be able to update an existing to-do item
  So that I can change its task or mark it as done.

  Scenario: Successfully update an existing to-do item
    Given the API has a to-do with id 1 and task "Learn TDD"
    And the user has prepared an update payload with task "Master TDD" and done status "true"
    When the user sends a PUT request to update the to-do with id 1
    Then the response status code should be 200
    And the response should contain the updated to-do with id 1, task "Master TDD", and done status "true"
    And the to-do with id 1 in the list should be fully updated with task "Master TDD" and done status "true"

  Scenario: Attempt to update a non-existent to-do item
    Given the API has a list of to-dos
    And the user has prepared an update payload with task "This task does not exist" and done status "false"
    When the user sends a PUT request to update the to-do with id 99
    Then the response status code should be 404
    And the response should contain a "not found" error message