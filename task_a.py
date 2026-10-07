"""Select the maximum number of deliveries that one driver can complete."""

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Delivery:
    id: str
    start_time: int
    finish_time: int


def read_deliveries(path: Path) -> list[Delivery]:
    """Read ID, start, finish rows; ignore blank lines and # comments."""
    deliveries = []
    ids = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        row = line.split("#", 1)[0].strip()
        if not row:
            continue
        fields = row.split()
        if len(fields) != 3:
            raise ValueError(f"Line {line_number}: expected ID start_time finish_time")
        delivery_id, start_text, finish_text = fields
        try:
            start, finish = int(start_text), int(finish_text)
        except ValueError as exc:
            raise ValueError(f"Line {line_number}: times must be integers") from exc
        if start >= finish:
            raise ValueError(f"Line {line_number}: start_time must be less than finish_time")
        if delivery_id in ids:
            raise ValueError(f"Line {line_number}: duplicate delivery ID {delivery_id}")
        ids.add(delivery_id)
        deliveries.append(Delivery(delivery_id, start, finish))
    return deliveries


def select_maximum_deliveries(deliveries: list[Delivery]) -> list[Delivery]:
    """Choose compatible deliveries in increasing finish-time order."""
    ordered = sorted(deliveries, key=lambda delivery: (
        delivery.finish_time, delivery.start_time, delivery.id
    ))
    selected = []
    last_finish = None
    for delivery in ordered:
        if last_finish is None or delivery.start_time >= last_finish:
            selected.append(delivery)
            last_finish = delivery.finish_time
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_file", type=Path, help="File containing ID start_time finish_time rows")
    args = parser.parse_args()
    try:
        selected = select_maximum_deliveries(read_deliveries(args.data_file))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print("Selected deliveries:")
    print("ID\tStart\tFinish")
    for delivery in selected:
        print(f"{delivery.id}\t{delivery.start_time}\t{delivery.finish_time}")
    print(f"Total deliveries completed: {len(selected)}")


if __name__ == "__main__":
    main()
