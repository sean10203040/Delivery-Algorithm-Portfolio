"""Assign every delivery using the minimum number of drivers."""

import argparse
import heapq
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Delivery:
    id: str
    start_time: int
    finish_time: int


def read_deliveries(path: Path) -> list[Delivery]:
    """Read whitespace-separated ID, start, finish rows."""
    deliveries = []
    ids = set()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fields = line.split("#", 1)[0].split()
        if not fields:
            continue
        if len(fields) != 3:
            raise ValueError(f"Line {number}: expected ID start_time finish_time")
        delivery_id, start_text, finish_text = fields
        try:
            start, finish = int(start_text), int(finish_text)
        except ValueError as exc:
            raise ValueError(f"Line {number}: times must be integers") from exc
        if start >= finish:
            raise ValueError(f"Line {number}: start_time must be less than finish_time")
        if delivery_id in ids:
            raise ValueError(f"Line {number}: duplicate delivery ID {delivery_id}")
        ids.add(delivery_id)
        deliveries.append(Delivery(delivery_id, start, finish))
    return deliveries


def assign_minimum_drivers(deliveries: list[Delivery]) -> list[list[Delivery]]:
    """Process deliveries by start time, reusing the earliest available driver."""
    ordered = sorted(deliveries, key=lambda d: (d.start_time, d.finish_time, d.id))
    schedules: list[list[Delivery]] = []
    # One entry per driver: (finish time of their latest delivery, driver index).
    availability: list[tuple[int, int]] = []
    for delivery in ordered:
        if availability and availability[0][0] <= delivery.start_time:
            _, driver = heapq.heappop(availability)
        else:
            driver = len(schedules)
            schedules.append([])
        schedules[driver].append(delivery)
        heapq.heappush(availability, (delivery.finish_time, driver))
    return schedules


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_file", type=Path, help="File containing ID start_time finish_time rows")
    args = parser.parse_args()
    try:
        schedules = assign_minimum_drivers(read_deliveries(args.data_file))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    for number, schedule in enumerate(schedules, 1):
        entries = " ".join(f"{d.id} ({d.start_time},{d.finish_time})" for d in schedule)
        print(f"Driver {number}: {entries}")
    print(f"Minimum drivers required: {len(schedules)}")


if __name__ == "__main__":
    main()
