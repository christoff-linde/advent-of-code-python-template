"""Solution runner and benchmarking utilities."""

import importlib.util
import sys
import time
from pathlib import Path

from src.aoc_cli import read_input
from src.template import get_available_days


def run_day(day: int, year: int | None = None) -> None:
    """Run the solution for a specific day.

    Args:
        day: Day number (1-25)
        year: Optional year. If not provided, uses root src/solutions.
    """
    day_padded = f"{day:02d}"
    root = Path(__file__).parent.parent

    if year is None:
        module_path = (
            Path(__file__).parent / "solutions" / f"day{day_padded}.py"
        )
    else:
        module_path = root / str(year) / "solutions" / f"day{day_padded}.py"

    if not module_path.exists():
        print(f"✗ Error: Solution for day {day} not found", file=sys.stderr)
        sys.exit(1)

    try:
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(
            f"day{day_padded}", module_path
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load {module_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Read input and run solutions
        try:
            input_text = read_input(day, year)
        except FileNotFoundError:
            print(
                f"✗ Error: Input file not found for day {day}",
                file=sys.stderr,
            )
            sys.exit(1)

        data = module.parse_input(input_text)

        print(f"Day {day_padded}")
        print("-" * 40)

        start = time.perf_counter()
        result1 = module.part_one(data)
        time1 = time.perf_counter() - start

        start = time.perf_counter()
        result2 = module.part_two(data)
        time2 = time.perf_counter() - start

        print(f"Part 1: {result1} ({time1 * 1000:.2f}ms)")
        print(f"Part 2: {result2} ({time2 * 1000:.2f}ms)")

    except Exception as e:
        print(f"✗ Error running day {day}: {e}", file=sys.stderr)
        sys.exit(1)


def run_all(year: int | None = None) -> None:
    """Run all available solutions.

    Args:
        year: Optional year. If not provided, uses root src/solutions.
    """
    available_days = get_available_days(year)

    if not available_days:
        print("No solutions found")
        return

    root = Path(__file__).parent.parent
    total_time = 0
    print(f"Running {len(available_days)} days...")
    print("=" * 40)

    for day in available_days:
        day_padded = f"{day:02d}"

        if year is None:
            module_path = (
                Path(__file__).parent / "solutions" / f"day{day_padded}.py"
            )
        else:
            module_path = root / str(year) / "solutions" / f"day{day_padded}.py"

        try:
            spec = importlib.util.spec_from_file_location(
                f"day{day_padded}", module_path
            )
            if spec is None or spec.loader is None:
                print(f"✗ Day {day_padded}: Could not load module")
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            try:
                input_text = read_input(day, year)
            except FileNotFoundError:
                print(f"⊘ Day {day_padded}: Input file not found")
                continue

            data = module.parse_input(input_text)

            start = time.perf_counter()
            result1 = module.part_one(data)
            time1 = time.perf_counter() - start

            start = time.perf_counter()
            result2 = module.part_two(data)
            time2 = time.perf_counter() - start

            elapsed = time1 + time2
            total_time += elapsed

            print(
                f"Day {day_padded}: {result1}, {result2} "
                f"({elapsed * 1000:.2f}ms)"
            )

        except Exception as e:
            print(f"✗ Day {day_padded}: {e}")

    print("=" * 40)
    print(f"Total time: {total_time * 1000:.2f}ms")


def time_day(day: int, year: int | None = None) -> None:
    """Benchmark a specific day's solution using pytest.

    Args:
        day: Day number (1-25)
        year: Optional year. If not provided, uses root tests.
    """
    day_padded = f"{day:02d}"
    root = Path(__file__).parent.parent

    if year is None:
        test_path = root / "tests" / f"test_day{day_padded}.py"
    else:
        test_path = root / str(year) / "tests" / f"test_day{day_padded}.py"

    if not test_path.exists():
        print(f"✗ Error: Test file for day {day} not found", file=sys.stderr)
        sys.exit(1)

    import subprocess

    result = subprocess.run(
        [
            "uv",
            "run",
            "pytest",
            str(test_path),
            "-v",
            "-m",
            "benchmark",
            "--benchmark-only",
        ],
        cwd=root,
    )

    sys.exit(result.returncode)


def time_all(year: int | None = None) -> None:
    """Benchmark all available solutions using pytest.

    Args:
        year: Optional year. If not provided, uses root tests.
    """
    available_days = get_available_days(year)

    if not available_days:
        print("No solutions found")
        return

    root = Path(__file__).parent.parent

    if year is None:
        test_dir = "tests/"
    else:
        test_dir = f"{year}/tests/"

    import subprocess

    result = subprocess.run(
        [
            "uv",
            "run",
            "pytest",
            test_dir,
            "-v",
            "-m",
            "benchmark",
            "--benchmark-only",
        ],
        cwd=root,
    )

    sys.exit(result.returncode)
