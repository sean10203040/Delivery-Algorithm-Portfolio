"""The six required Task A cases, plus input and boundary checks."""

import tempfile
import unittest
from pathlib import Path

from task_a import Delivery, read_deliveries, select_maximum_deliveries


REQUIRED_CASES = [
    ([], 0),
    ([(1, 3)], 1),
    ([(1, 3), (3, 5), (5, 7)], 3),
    ([(1, 5), (2, 6), (3, 7)], 1),
    ([(5, 7), (1, 3), (3, 5), (2, 4)], 3),
    ([(1, 4), (2, 4), (4, 6)], 2),
]


class TaskATests(unittest.TestCase):
    def test_required_cases(self):
        for number, (intervals, expected) in enumerate(REQUIRED_CASES, 1):
            with self.subTest(case=number):
                deliveries = [Delivery(f"D{i:02}", start, finish)
                              for i, (start, finish) in enumerate(intervals, 1)]
                selected = select_maximum_deliveries(deliveries)
                self.assertEqual(len(selected), expected)
                self.assertTrue(all(a.finish_time <= b.start_time
                                    for a, b in zip(selected, selected[1:])))
                self.assertTrue(all(delivery in deliveries for delivery in selected))

    def test_negative_times(self):
        deliveries = [Delivery("A", -5, -2), Delivery("B", -2, 0)]
        self.assertEqual(select_maximum_deliveries(deliveries), deliveries)

    def test_file_input_and_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "deliveries.txt"
            path.write_text("# deliveries\n\nD01 1 3\nD02 3 5 # back-to-back\n", encoding="utf-8")
            self.assertEqual(len(select_maximum_deliveries(read_deliveries(path))), 2)
            for invalid in ("D01 3 3", "D01 x 4", "D01 1", "D01 1 3\nD01 3 5"):
                with self.subTest(invalid=invalid):
                    path.write_text(invalid, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        read_deliveries(path)


if __name__ == "__main__":
    unittest.main()
