Feature: Questions

  Scenario: Add new answer
    Given I am a visitor
    Given exists questions
    When I create answer "Good question!" to question
    Then I should see "Good question!" in page