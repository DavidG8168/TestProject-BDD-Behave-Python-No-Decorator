Feature: TestProject with Behave Framework

  Scenario: Run a Simple BDD test with TestProject
     Given I navigate to the TestProject example page
     When I perform a login
     Then I should see a logout button