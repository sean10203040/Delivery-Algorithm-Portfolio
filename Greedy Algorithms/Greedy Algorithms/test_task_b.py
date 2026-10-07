"""Check Task B counts, complete assignment, and conflict-free schedules."""

import unittest
from collections import Counter

from task_b import Delivery, assign_minimum_drivers


class TaskBTests(unittest.TestCase):
    def test_required_cases(self):
        cases = [
            ([], 0),
            ([(1, 3)], 1),
            ([(1, 3), (3, 5), (5, 7)], 1),
            ([(1, 5), (2, 6), (3, 7)], 3),
            ([(1, 4), (2, 5), (4, 7), (5, 8)], 2),
            ([(5, 8), (1, 4), (2, 5), (4, 6), (6, 9)], 2),
        ]
        for number, (intervals, expected) in enumerate(cases, 1):
            with self.subTest(case=number):
                deliveries = [Delivery(f"D{i:02}", start, finish)
                              for i, (start, finish) in enumerate(intervals, 1)]
                schedules = assign_minimum_drivers(deliveries)
                self.assertEqual(len(schedules), expected)
                self.assertEqual(Counter(d for s in schedules for d in s), Counter(deliveries))
                for schedule in schedules:
                    self.assertTrue(all(a.finish_time <= b.start_time
                                        for a, b in zip(schedule, schedule[1:])))


if __name__ == "__main__":
    unittest.main()
