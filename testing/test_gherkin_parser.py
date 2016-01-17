import gherkin_parser as gp
import unittest

import io
import os


class TestUpdateSteps(unittest.TestCase):

    def test_get_feature_files_valid_folder(self):
        directory = os.getcwd() + '/testing/feature-files'
        actual = gp.get_feature_files([directory])
        expected = [os.path.join(directory, f) for f in os.listdir(directory)]
        self.assertEqual(actual, expected)

    def test_get_feature_files_invalid_folder(self):
        directory = os.getcwd() + '/a-fake-folder-name/'
        actual = gp.get_feature_files([directory])
        expected = []
        self.assertEqual(actual, expected)

    def test_get_steps_one_file(self):
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
        actual = gp.get_steps([sio])
        expected = set([
            ('given', 'there is a coffee named "Sublime"'),
            ('given', 'the coffee costs 1.50 dollars'),
            ('when', 'I give the cashier 2 dollars'),
            ('when', "I say 'Good Morning!'"),
            ('then', 'I should receive the <AMAZING> coffee'),
            ('then', 'I should receive 0.50 in change')
        ])
        self.assertEqual(actual, expected)

    def test_get_steps_multiple_files(self):
        sio1 = io.StringIO(
            """Feature: Coffee Testing

                Scenario: Buy first Coffee
                    Given there is a coffee named "Sublime"
                    When I give the cashier 2 dollars
                    Then I should receive the <AMAZING> coffee"""
        )
        sio2 = io.StringIO(
            """Feature: More Coffee Testing

                Scenario: Buy first Coffee
                    Given some different steps
                    When I type more steps
                    Then I get more steps"""
        )
        actual = gp.get_steps([sio1, sio2])
        expected = set([
            ('given', 'there is a coffee named "Sublime"'),
            ('when', 'I give the cashier 2 dollars'),
            ('then', 'I should receive the <AMAZING> coffee'),
            ('given', 'some different steps'),
            ('when', 'I type more steps'),
            ('then', 'I get more steps')
        ])
        self.assertEqual(actual, expected)

    def test_get_steps_table_skipped(self):
        sio = io.StringIO(
            """Feature: Coffee Testing

                Scenario: Buy first Coffee
                    | column1 | column2 | column3 |
                    | value1  | value2  | value3  |
            """
        )
        actual = gp.get_steps([sio])
        expected = set()
        self.assertEqual(actual, expected)

    def test_get_steps_comment_skipped(self):
        sio = io.StringIO(
            """Feature: Coffee Testing

                Scenario: Buy first Coffee
                # Only a comment supplied
            """
        )
        actual = gp.get_steps([sio])
        expected = set()
        self.assertEqual(actual, expected)

    def test_get_steps_syntax_error_in_file(self):
        sio = io.StringIO(
            """Feature: More Coffee Testing

                Scenario: Buy first Coffee
                    Given a valid step
                    And
                    When a step after an error
            """
        )
        actual = gp.get_steps([sio])
        expected = set([
            ('given', 'a valid step'),
            ('when', 'a step after an error')
        ])
        self.assertEqual(actual, expected)

    def test_format_steps_valid_input(self):
        unformatted_steps = set([
            ('given', 'there is a coffee named "Sublime"'),
            ('given', 'the coffee costs 1.50 dollars'),
            ('when', 'I give the cashier 2 dollars'),
            ('when', "I say 'Good Morning!'"),
            ('then', 'I should receive the <AMAZING> coffee'),
            ('then', 'I should receive 0.50 in change')
        ])
        actual = gp.format_steps(unformatted_steps)
        expected = set([
            ('given', 'there is a coffee named "input"'),
            ('given', 'the coffee costs [number] dollars'),
            ('when', 'I give the cashier [number] dollars'),
            ('when', "I say 'input'"),
            ('then', 'I should receive the <input> coffee'),
            ('then', 'I should receive [number] in change')
        ])
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
