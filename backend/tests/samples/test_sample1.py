import unittest
from tests import BaseTestCase
from tests.utils.sample1 import (
    add_two_numbers,
    substract_two_numbers,
    multiply_two_numbers,
    division_two_numbers
)


class TestExample1(BaseTestCase):
    """ Example test for dummy purposes """

    def setUp(self):
        """ Setting up the test case """
        super().setUp()
        self.n1 = 4
        self.n2 = 4

    def test_add_two_numbers(self):
        """ Test adding two numbers ok """
        result = self.n1 + self.n2
        self.assertEqual(
            result,
            add_two_numbers(self.n1, self.n2)
        )

    def test_substract_two_numbers(self):
        """ Test substracting two numbers """
        result = self.n1 - self.n2
        self.assertEqual(
            result, substract_two_numbers(self.n1, self.n2)

        )
    
    def test_multiply_two_numbers(self):
        """ Test Multiply two numbers """
        result = self.n1 * self.n2
        self.assertEqual(
            result, multiply_two_numbers(self.n1, self.n2)
        )

    def test_division_two_numbers(self):
        """ Test division of two numbers """
        result = self.n1 / self.n2
        self.assertEqual(
            result, division_two_numbers(self.n1, self.n2)
        )



if __name__ == "__main__":
    unittest.main()
