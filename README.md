# Pioneer Delivery Algorithm Portfolio: Tasks A, B, and C

This Python implementation selects the maximum number of non-overlapping
deliveries that one driver can complete. It outputs each selected delivery's ID,
start time, finish time, and the total number selected.

## Requirements and running

Python 3.10 or newer is required. No third-party packages or compilation are needed.

```text
python task_a.py deliveries.txt
python task_b.py deliveries.txt
python task_c.py deliveries.txt
python -m unittest -v test_task_a test_task_b test_task_c
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
invalid input.

## Task B: Minimum number of drivers

`task_b.py` is a standalone program using the same input-file format and sample
data as Task A. It prints each driver's delivery IDs and intervals, followed by
the minimum driver count. Its `Delivery` and `read_deliveries` handle input,
`assign_minimum_drivers` implements the algorithm, and `main` prints schedules.
It does not depend on the filename of the Task A script.

### Priority queue and greedy choice

Sort deliveries by increasing start time. Maintain a min-heap of pairs
`(latest_finish_time, driver_index)`, with exactly one entry per existing driver.
The heap's root identifies the driver available earliest. If that driver finishes
at or before the next delivery's start, remove their entry and reuse them.
Otherwise, create a new driver. Append the delivery to that driver's schedule
and push their updated finish time into the heap. Equal finish times use the
driver index to break ties. Back-to-back deliveries can share a driver.

### Why the driver count is minimum

Whenever a new driver is created for a delivery starting at time s, the earliest
driver finish time is greater than s. Therefore every existing driver has a
delivery still in progress at s. Because requests are processed in start-time
order, those deliveries have all started by s. They overlap each other and the
new request at s, so every valid schedule needs at least this many drivers.
The algorithm creates a driver only when this lower bound requires it, and
reusing a driver never creates a conflict. Its driver count is thus optimal.
For no deliveries, zero drivers are required.

### Running time and space

Sorting takes O(n log n). Each request performs at most one heap removal and
one insertion, each taking O(log n). Total time is O(n log n). The sorted input,
heap, and output schedules use O(n) space.

### Required Task B test results

| Test | Delivery intervals | Expected drivers | Actual drivers |
| --- | --- | --- | --- |
| 1 | No deliveries | 0 | 0 |
| 2 | (1,3) | 1 | 1 |
| 3 | (1,3), (3,5), (5,7) | 1 | 1 |
| 4 | (1,5), (2,6), (3,7) | 3 | 3 |
| 5 | (1,4), (2,5), (4,7), (5,8) | 2 | 2 |
| 6 | (5,8), (1,4), (2,5), (4,6), (6,9) | 2 | 2 |

`test_task_b.py` checks all six counts, verifies every delivery is assigned
exactly once, and checks that each driver's schedule has no overlaps.

## Task C: Minimum rejected deliveries

`task_c.py` reads the same input format and prints the minimum number of rejected
deliveries. It imports `Delivery`, `read_deliveries`, and
`select_maximum_deliveries` from `task_a.py`, so keep that file with its original
name in the same folder. `minimum_rejected_deliveries` calculates the answer;
`main` handles input and output.

### Relationship to Task A and correctness

Task A finds a maximum compatible subset of k deliveries among n requests.
Task C keeps that subset and rejects the other n - k requests. This leaves a
valid schedule. Rejecting fewer would leave more than k compatible deliveries,
contradicting the fact that k is the maximum. Therefore the minimum number
rejected is n - k. Empty input gives 0 - 0 = 0 rejections.

### Running time and space

Task C calls Task A's O(n log n) greedy algorithm, then subtracts the selected
count from the input count in O(1) time. Total time is O(n log n), with O(n)
space for the input and Task A's sorted and selected lists.

### Required Task C test results

| Test | Delivery intervals | Expected rejected | Actual rejected |
| --- | --- | --- | --- |
| 1 | No deliveries | 0 | 0 |
| 2 | (1,3) | 0 | 0 |
| 3 | (1,3), (3,5), (5,7) | 0 | 0 |
| 4 | (1,5), (2,6), (3,7) | 2 | 2 |
| 5 | (5,7), (1,3), (3,5), (2,4) | 1 | 1 |
| 6 | (1,2), (2,3), (3,4), (1,3) | 1 | 1 |

`test_task_c.py` verifies the six required rejection counts. The sample data
contains seven deliveries, of which Task A selects three, so Task C reports
four rejections.

## Task D: When a greedy choice fails

Consider these three deliveries. Each takes exactly one unit of time, all ready
times are nonnegative integers, and the positive profits are distinct.

| Delivery | Ready time R | Profit P |
| --- | --- | --- |
| A | 0 | 10 |
| B | 0 | 9 |
| C | 1 | 8 |

A delivery assigned to slot T has delay D = T - R and contributes
V = P / (1 + D). Slots 0, 1, and 2 represent [0,1), [1,2), and [2,3).

### Schedule produced by greedy strategy G

The strategy considers A, B, and C in decreasing profit order. It puts A in
slot 0, B in slot 1 (the earliest unused slot at or after B's ready time 0),
and C in slot 2 (the earliest unused slot at or after C's ready time 1).

| Delivery | Assigned slot T | Delay T - R | Value P / (1 + D) |
| --- | --- | --- | --- |
| A | 0 | 0 | 10 |
| B | 1 | 1 | 9/2 |
| C | 2 | 1 | 4 |

V(G) = 10 + 9/2 + 4 = 37/2 = 18.5.

### A better schedule S

Keep A in slot 0, put C in slot 1, and put B in slot 2. Every delivery is
scheduled at or after its ready time, and the assigned slots are distinct.

| Delivery | Assigned slot T | Delay T - R | Value P / (1 + D) |
| --- | --- | --- | --- |
| A | 0 | 0 | 10 |
| C | 1 | 0 | 8 |
| B | 2 | 2 | 3 |

V(S) = 10 + 8 + 3 = 21.

### Why this disproves optimality

V(S) = 21 > 18.5 = V(G), so the proposed greedy strategy does not always
produce an optimal schedule. Moving B from slot 1 to slot 2 loses only 1.5
in value, while moving C from slot 2 to slot 1 gains 4. The total improves
by 2.5. Profit alone does not account for these different effects of delay.
A better valid schedule is sufficient to disprove optimality; it is not
necessary to prove that S is the best possible schedule.
