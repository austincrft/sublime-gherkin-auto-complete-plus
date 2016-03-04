Feature: Coffee Testing

  Scenario: Buy first Coffee
      Given there is a coffee named "Sublime"
      And the coffee costs 1.50 dollars
      When I give the cashier 2 dollars
      And I say 'Good Morning!'
      Then I should receive the <AMAZING> coffee
      And I should receive 0.50 in change
