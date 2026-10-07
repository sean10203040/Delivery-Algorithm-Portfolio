# Pioneer Delivery Algorithm Portfolio: Task A

This Python implementation selects the maximum number of non-overlapping
deliveries that one driver can complete. It outputs each selected delivery's ID,
start time, finish time, and the total number selected.

## Requirements and running

Python 3.10 or newer is required. No third-party packages or compilation are needed.

```text
python task_a.py deliveries.txt
python -m unittest -v test_task_a
```

On Windows, `py` can be used instead of `python` if that is your installed launcher.

## Input format

Each row contains a unique delivery ID followed by integer start and finish times,
separated by whitespace. Start must be less than finish. Blank lines and comments
beginning with `#` are ignored. An empty file represents no deliveries.

```text
D01 10 13
D02 2 5
```

`deliveries.txt` contains the seven example requests from the assignment.
For that file, the program selects D02 (2,5), D05 (8,11), and D06 (11,14),
for a total of three deliveries.

## Program organization

- `Delivery` stores a request's ID and time interval.
- `read_deliveries` reads and validates the input file.
- `select_maximum_deliveries` implements the greedy algorithm.
- `main` handles command-line arguments and prints results.
- `test_task_a.py` verifies the required cases and input handling.

## Greedy choice

Sort requests by increasing finish time. Choose the first request, then repeatedly
choose the next request whose start time is at least the finish time of the last
selected request. Choosing the earliest finishing compatible delivery leaves
the most time available for future deliveries. Equal finish times are ordered by
start time and ID for reproducible output; any optimal schedule is acceptable.

The compatibility comparison uses `>=`, so back-to-back deliveries are allowed.

## Why the algorithm is optimal

Let g be the delivery with the earliest finish time, and let o be the first
delivery in an optimal schedule. Because g finishes no later than o, replacing
o with g keeps every later delivery compatible and preserves the schedule's
number of deliveries. Therefore, some optimal schedule begins with g.

After choosing g, the remaining problem consists of deliveries starting at or
after g's finish time. The same replacement argument applies to this smaller
problem. Repeating the argument proves that all greedy choices can form an
optimal schedule. The empty input has the optimal count of zero.

## Running time and space

Sorting takes O(n log n), and scanning the sorted requests takes O(n), giving
O(n log n) total time. The input, sorted list, and selected list use O(n) space.

## Required test results

IDs D01, D02, etc. correspond to each interval's position in its test input.

| Test | Delivery intervals | Expected count | Actual count | Selected IDs |
| --- | --- | --- | --- | --- |
| 1 | No deliveries | 0 | 0 | None |
| 2 | (1,3) | 1 | 1 | D01 |
| 3 | (1,3), (3,5), (5,7) | 3 | 3 | D01, D02, D03 |
| 4 | (1,5), (2,6), (3,7) | 1 | 1 | D01 |
| 5 | (5,7), (1,3), (3,5), (2,4) | 3 | 3 | D02, D03, D01 |
| 6 | (1,4), (2,4), (4,6) | 2 | 2 | D01, D03 |

The automated tests check the selected count, compatibility, and membership in
the input. Additional checks cover negative integer times, file parsing, and
invalid input. Tasks B, C, and D are not implemented in this Task A submission.
