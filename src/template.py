"""Template management for scaffolding new day solutions."""

import json
from pathlib import Path

from src.aoc_cli import download_input, download_puzzle


def load_config() -> dict:
    """Load configuration from .aoc-cli.json."""
    config_path = Path(__file__).parent.parent / ".aoc-cli.json"
    with open(config_path) as f:
        return json.load(f)


def read_template() -> str:
    """Read the solution template file."""
    template_path = Path(__file__).parent / "solutions" / "template.txt"
    return template_path.read_text()


def get_solutions_dir(year: int | None = None) -> Path:
    """Get solutions directory, optionally for a specific year."""
    root = Path(__file__).parent.parent
    if year is None:
        return root / "src" / "solutions"
    return root / str(year) / "solutions"


def get_tests_dir(year: int | None = None) -> Path:
    """Get tests directory, optionally for a specific year."""
    root = Path(__file__).parent.parent
    if year is None:
        return root / "tests"
    return root / str(year) / "tests"


def scaffold_day(day: int, download: bool = False) -> tuple[Path, Path, Path]:
    """
    Scaffold files for a new day.

    Args:
        day: Day number (1-25)
        download: Whether to download input/puzzle using aoc-cli

    Returns:
        Tuple of (solution_path, test_path, example_path)
    """
    config = load_config()
    year = config.get("year", 2025)
    day_padded = f"{day:02d}"
    root = Path(__file__).parent.parent

    # Year-based paths
    year_dir = root / str(year)
    solutions_dir = year_dir / "solutions"
    tests_dir = year_dir / "tests"
    data_dir = year_dir / "data"

    # File paths
    solution_path = solutions_dir / f"day{day_padded}.py"
    test_path = tests_dir / f"test_day{day_padded}.py"
    example_path = data_dir / "examples" / f"{day_padded}.txt"
    input_path = data_dir / "inputs" / f"{day_padded}.txt"
    puzzle_path = data_dir / "puzzles" / f"{day_padded}.md"

    # Check if already exists
    if solution_path.exists():
        raise FileExistsError(f"Solution for day {day} already exists")

    # Download input and puzzle if requested
    if download:
        try:
            download_input(day, year)
            download_puzzle(day, year)
        except Exception as e:
            print(f"Warning: Could not download data: {e}")
            # Continue scaffolding even if download fails

    # Create directories
    solutions_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "examples").mkdir(parents=True, exist_ok=True)
    (data_dir / "inputs").mkdir(parents=True, exist_ok=True)
    (data_dir / "puzzles").mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    (solutions_dir / "__init__.py").touch()
    (tests_dir / "__init__.py").touch()

    # Create conftest.py for year folder if it doesn't exist
    conftest_path = tests_dir / "conftest.py"
    if not conftest_path.exists():
        conftest_content = '''"""Pytest configuration for year folder."""

import re
import sys
from pathlib import Path

import pytest

from src.aoc_cli import read_example

# Add year solutions to path so imports work
year_dir = Path(__file__).parent.parent
sys.path.insert(0, str(year_dir))


@pytest.fixture
def example(request):
    """
    Load example input automatically from data/examples/{day}.txt.

    Extracts the day number from the test file name (e.g., test_day01.py -> 01)
    and loads the corresponding example file from the year-specific data dir.
    """
    test_file = Path(request.fspath).name  # e.g., "test_day01.py"
    match = re.search(r"day(\\d+)", test_file)
    if not match:
        raise ValueError(f"Could not extract day number from {test_file}")

    day = int(match.group(1))
    year_dir_obj = Path(__file__).parent.parent
    return read_example(day, int(year_dir_obj.name))
'''
        conftest_path.write_text(conftest_content)

    # Create solution file
    template = read_template()
    solution_content = template.format(
        year=year, day=day, day_padded=day_padded
    )
    solution_path.write_text(solution_content)

    # Create test file
    test_content = f'''"""Tests for Day {day_padded}."""

import sys
from pathlib import Path

import pytest

# Add year solutions to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from solutions.day{day_padded} import parse_input, part_one, part_two


def test_parse_input(example):
    """Test input parsing."""
    data = parse_input(example)
    assert data is not None


def test_part_one(example):
    """Test part one with example data."""
    data = parse_input(example)
    result = part_one(data)
    assert result == 0  # Update with expected value


def test_part_two(example):
    """Test part two with example data."""
    data = parse_input(example)
    result = part_two(data)
    assert result == 0  # Update with expected value


@pytest.mark.benchmark
def test_benchmark_part_one(benchmark):
    """Benchmark part one."""
    from src.aoc_cli import read_input

    try:
        input_text = read_input({day}, {year})
        data = parse_input(input_text)
        benchmark(part_one, data)
    except FileNotFoundError:
        pytest.skip("Input file not found")


@pytest.mark.benchmark
def test_benchmark_part_two(benchmark):
    """Benchmark part two."""
    from src.aoc_cli import read_input

    try:
        input_text = read_input({day}, {year})
        data = parse_input(input_text)
        benchmark(part_two, data)
    except FileNotFoundError:
        pytest.skip("Input file not found")
'''
    test_path.write_text(test_content)

    # Create empty example file if it doesn't exist
    if not example_path.exists():
        example_path.touch()

    # Create empty input/puzzle files if they don't exist and weren't downloaded
    if not input_path.exists():
        input_path.touch()
    if not puzzle_path.exists():
        puzzle_path.touch()

    return solution_path, test_path, example_path


def get_available_days(year: int | None = None) -> list[int]:
    """Get list of days that have been scaffolded.

    Args:
        year: Optional year to filter. If not provided, checks root src/solutions.

    Returns:
        Sorted list of available day numbers.
    """
    if year is None:
        solutions_dir = Path(__file__).parent / "solutions"
    else:
        solutions_dir = Path(__file__).parent.parent / str(year) / "solutions"

    days = []

    for file in solutions_dir.glob("day*.py"):
        try:
            day_num = int(file.stem.replace("day", ""))
            days.append(day_num)
        except ValueError:
            continue

    return sorted(days)
