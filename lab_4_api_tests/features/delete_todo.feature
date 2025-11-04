Feature: Delete a To-Do item
  As a user of the API,
  I want to delete an existing to-do item by its ID,
  so that I can remove it from the list.

  Scenario: An existing to-do item is deleted
    Given the API has a to-do with id 1 and task "Learn TDD"
    When the user sends a DELETE request for the to-do with id 1
    Then the response status code should be 204
    And the to-do with id 1 should no longer be in the list

  Scenario: A non-existent to-do item cannot be deleted
    Given the API has a list of to-dos
    When the user sends a DELETE request for the to-do with id 99
    Then the response status code should be 404
    And the list of to-dos should be unchanged