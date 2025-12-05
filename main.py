"""Main entry point for Advent of Code solutions."""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.aoc_cli import (
    check_aoc_cli,
    download_input,
    download_puzzle,
    read_puzzle,
)
from src.runner import run_all, run_day, time_all, time_day
from src.template import load_config, scaffold_day


def main():
    """Main CLI entry point."""
    config = load_config()
    year = config.get("year", 2025)

    parser = argparse.ArgumentParser(
        description="Advent of Code Python Solutions"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Global year option
    parser.add_argument(
        "--year",
        type=int,
        default=year,
        help=f"Year (default: {year})",
    )

    # Scaffold command
    scaffold_parser = subparsers.add_parser(
        "scaffold", help="Scaffold a new day"
    )
    scaffold_parser.add_argument("day", type=int, help="Day number (1-25)")
    scaffold_parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download input and puzzle",
    )

    # Download command
    download_parser = subparsers.add_parser(
        "download", help="Download input and puzzle"
    )
    download_parser.add_argument("day", type=int, help="Day number (1-25)")
    download_parser.add_argument(
        "--input-only", action="store_true", help="Only download input"
    )
    download_parser.add_argument(
        "--puzzle-only", action="store_true", help="Only download puzzle"
    )

    # Read command (mirrors Rust template)
    read_parser = subparsers.add_parser("read", help="Print puzzle description")
    read_parser.add_argument("day", type=int, help="Day number (1-25)")

    # Solve/run command
    solve_parser = subparsers.add_parser("solve", help="Run solution for a day")
    solve_parser.add_argument("day", type=int, help="Day number (1-25)")
    solve_parser.add_argument(
        "--release",
        action="store_true",
        help="Run with optimizations (future use)",
    )

    # Run all command
    subparsers.add_parser("all", help="Run all solutions")

    # Time command
    time_parser = subparsers.add_parser(
        "time", help="Benchmark a day's solution"
    )
    time_parser.add_argument(
        "day", type=int, nargs="?", help="Day number (1-25)"
    )
    time_parser.add_argument("--all", action="store_true", help="Time all days")

    args = parser.parse_args()

    # Use the year from args (either default or --year flag)
    current_year = args.year if hasattr(args, "year") else year

    if args.command == "scaffold":
        try:
            solution_path, test_path, example_path = scaffold_day(
                args.day, download=args.download
            )
            print(f"✓ Scaffolded day {args.day:02d}")
            print(f"  Solution: {solution_path}")
            print(f"  Tests: {test_path}")
            print(f"  Example: {example_path}")
            if args.download:
                print("  Input and puzzle downloaded")
        except FileExistsError as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "download":
        try:
            if not check_aoc_cli():
                print("✗ Error: aoc-cli not installed", file=sys.stderr)
                print("Install with: cargo install aoc-cli", file=sys.stderr)
                print(
                    "Configure with: aoc credentials -s <session_cookie>",
                    file=sys.stderr,
                )
                sys.exit(1)

            if not args.puzzle_only:
                download_input(args.day, current_year)
                print(f"✓ Downloaded input for day {args.day:02d}")

            if not args.input_only:
                download_puzzle(args.day, current_year)
                print(f"✓ Downloaded puzzle for day {args.day:02d}")
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "read":
        try:
            puzzle = read_puzzle(args.day, current_year)
            print(puzzle)
        except FileNotFoundError as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "solve":
        run_day(args.day, current_year)

    elif args.command == "all":
        run_all(current_year)

    elif args.command == "time":
        if args.all:
            time_all(current_year)
        elif args.day:
            time_day(args.day, current_year)
        else:
            print("✗ Error: Specify a day or use --all", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
