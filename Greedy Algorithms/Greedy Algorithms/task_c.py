"""Find the minimum deliveries to reject so one driver can handle the rest."""

import argparse
from pathlib import Path

from task_a import Delivery, read_deliveries, select_maximum_deliveries


def minimum_rejected_deliveries(deliveries: list[Delivery]) -> int:
    """Reject everything outside a maximum compatible subset."""
    return len(deliveries) - len(select_maximum_deliveries(deliveries))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_file", type=Path, help="File containing ID start_time finish_time rows")
    args = parser.parse_args()
    try:
        rejected = minimum_rejected_deliveries(read_deliveries(args.data_file))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Minimum deliveries rejected: {rejected}")


if __name__ == "__main__":
    main()
