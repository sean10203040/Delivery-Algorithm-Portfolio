"""The six required Task C cases."""

import unittest

from task_a import Delivery
from task_c import minimum_rejected_deliveries


class TaskCTests(unittest.TestCase):
    def test_required_cases(self):
        cases = [
            ([], 0),
            ([(1, 3)], 0),
            ([(1, 3), (3, 5), (5, 7)], 0),
            ([(1, 5), (2, 6), (3, 7)], 2),
            ([(5, 7), (1, 3), (3, 5), (2, 4)], 1),
            ([(1, 2), (2, 3), (3, 4), (1, 3)], 1),
        ]
        for number, (intervals, expected) in enumerate(cases, 1):
            with self.subTest(case=number):
                deliveries = [Delivery(f"D{i:02}", start, finish)
                              for i, (start, finish) in enumerate(intervals, 1)]
                self.assertEqual(minimum_rejected_deliveries(deliveries), expected)


if __name__ == "__main__":
    unittest.main()
