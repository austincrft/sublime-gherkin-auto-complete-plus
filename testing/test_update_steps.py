import update_steps as us

import unittest
import io


class TestUpdateSteps(unittest.TestCase):
    def setUp(self):
        self.unformatted_steps = set([
            ('given', 'there is a coffee named "Sublime"'),
            ('given', 'the coffee costs 1.50 dollars'),
            ('when', 'I give the cashier 2 dollars'),
            ('when', "I say 'Good Morning!'"),
            ('then', 'I should receive the <AMAZING> coffee'),
            ('then', 'I should receive 0.50 in change')
        ])

    def test_get_steps_valid_input(self):
        sio = io.StringIO(
            """Feature: Coffee Testing

                Scenario: Buy first Coffee
                    Given there is a coffee named "Sublime"
                    And the coffee costs 1.50 dollars
                    When I give the cashier 2 dollars
                    And I say 'Good Morning!'
                    Then I should receive the <AMAZING> coffee
                    And I should receive 0.50 in change"""
        )
        actual = us._get_steps([sio])
        self.assertEqual(actual, self.unformatted_steps)

    def test_format_steps_valid_input(self):
        expected = set([
            ('given', 'there is a coffee named "input"'),
            ('given', 'the coffee costs [number] dollars'),
            ('when', 'I give the cashier [number] dollars'),
            ('when', "I say 'input'"),
            ('then', 'I should receive the <input> coffee'),
            ('then', 'I should receive [number] in change')
        ])
        actual = us._format_steps(self.unformatted_steps)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
