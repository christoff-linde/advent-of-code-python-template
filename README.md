# Advent of Code Python Solutions

Solutions for [Advent of Code](https://adventofcode.com/) challenges implemented in Python with testing, benchmarking, and CLI scaffolding.

## Quick Start (5 minutes)

### Prerequisites

- Python 3.14+ ([Download](https://www.python.org/downloads/))
- [UV](https://docs.astral.sh/uv/getting-started/installation/) - Fast Python package manager
- [Cargo](https://www.rust-lang.org/tools/install) - To install aoc-cli
- [aoc-cli](https://github.com/scarvalhojr/aoc-cli) - Advent of Code CLI tool

### Initial Setup

```bash
# 1. Install aoc-cli (one-time)
cargo install aoc-cli

# 2. Get your session cookie and configure aoc-cli
# Visit https://adventofcode.com/ → login → Open DevTools (F12)
# Go to: Application/Storage → Cookies → Find 'session' cookie
aoc credentials -s <your_session_cookie>

# 3. Clone and setup this project
git clone <repository-url>
cd advent-of-code-python
uv sync
```

### Solve Your First Day

```bash
# Scaffold day 1 with template files and download input/puzzle
python main.py scaffold 1 --download

# Read the puzzle while coding
python main.py read 1

# Edit and implement your solution
# File: 2025/solutions/day01.py
# - Implement: parse_input(), part_one(), part_two()

# Run your solution
python main.py solve 1

# Run tests
make test
```

## Project Structure

```
advent-of-code-python/
├── src/                     # Shared source code
│   ├── aoc_cli.py          # aoc-cli integration & downloads
│   ├── template.py         # Day scaffolding utilities
│   ├── runner.py           # Solution execution & benchmarking
│   ├── solutions/          # Solution templates
│   │   ├── template.txt    # Template for new days
│   │   └── __init__.py
│   └── __init__.py
│
├── 2025/                    # Year-specific folder (configurable in .aoc-cli.json)
│   ├── solutions/          # Day solutions for 2025
│   │   ├── day01.py        # Your solution for day 1
│   │   ├── day02.py        # Your solution for day 2
│   │   └── __init__.py
│   ├── tests/              # Tests for 2025
│   │   ├── test_day01.py   # Tests for day 1
│   │   ├── test_day02.py   # Tests for day 2
│   │   ├── conftest.py     # Shared test fixtures
│   │   └── __init__.py
│   └── data/               # Data for 2025
│       ├── inputs/         # Downloaded puzzle inputs
│       ├── puzzles/        # Downloaded puzzle descriptions
│       └── examples/       # Example data (manually added)
│
├── 2024/                    # Previous year (optional)
│   ├── solutions/
│   ├── tests/
│   └── data/
│
├── main.py                 # CLI entry point
├── Makefile                # Common commands
├── pyproject.toml          # Dependencies & config
├── .aoc-cli.json          # aoc-cli config (year setting)
└── README.md               # This file
```

## Commands

### Scaffolding & Downloading

```bash
# Create a new day with template files (uses year from .aoc-cli.json)
python main.py scaffold <day>

# Create a day and download input/puzzle
python main.py scaffold <day> --download

# Create a day for a different year
python main.py --year 2024 scaffold <day>

# Download input and puzzle separately
python main.py download <day>
python main.py download <day> --input-only
python main.py download <day> --puzzle-only

# View puzzle description
python main.py read <day>
```

### Running Solutions

```bash
# Run a specific day's solution
python main.py solve <day>

# Run all scaffolded solutions
python main.py all
```

### Testing & Benchmarking

```bash
# Run all tests (auto-discovers year folders)
make test

# Run tests with verbose output
uv run pytest -v

# Run tests for a specific day
uv run pytest 2025/tests/test_day01.py -v

# Run only benchmark tests
make benchmark-all

# Benchmark a specific day
make benchmark day=1

# Run all tests without benchmarks
uv run pytest -v -m "not benchmark"
```

### Code Quality

```bash
# Check code style
make lint

# Format code automatically
make format

# Fix common issues
uv run ruff check --fix
```

## Make Commands (Optional)

For convenience, use `make` for common tasks:

```bash
make help                       # Show all commands
make scaffold day=1             # Scaffold day 1 (auto-downloads input)
make download day=1             # Download day 1 data only
make solve day=1                # Run day 1 solution
make run                        # Run all solutions
make test                       # Run all tests (includes benchmarks)
make benchmark day=1            # Benchmark day 1 only
make benchmark-all              # Benchmark all days
make lint                       # Check code style
make format                     # Format code
make clean                      # Clean cache & temp files
```

## Solution Template

Each day follows this structure:

```python
"""Advent of Code 2025 - Day 1"""


def parse_input(input_text: str):
    """Parse the input data."""
    return input_text.strip().split('\n')


def part_one(data) -> int:
    """Solve part one."""
    # Your implementation here
    return 0


def part_two(data) -> int:
    """Solve part two."""
    # Your implementation here
    return 0


if __name__ == "__main__":
    from src.aoc_cli import read_input

    input_text = read_input(1, 2025)  # Year parameter for year-specific data
    data = parse_input(input_text)
    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
```

## Testing

Tests are auto-generated when you scaffold a day. The fixture automatically loads example data:

```python
"""Tests for Day 01."""

import sys
from pathlib import Path

import pytest

# Add year solutions to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from solutions.day01 import parse_input, part_one, part_two


def test_parse_input(example):  # 'example' fixture auto-loads from 2025/data/examples/01.txt
    """Test input parsing."""
    data = parse_input(example)
    assert data is not None


def test_part_one(example):
    """Test part one with example data."""
    data = parse_input(example)
    result = part_one(data)
    assert result == 3  # Update with expected value


@pytest.mark.benchmark
def test_benchmark_part_one(benchmark):
    """Benchmark part one (uses year-specific input)."""
    from src.aoc_cli import read_input

    input_text = read_input(1, 2025)  # Year parameter for year-specific data
    data = parse_input(input_text)
    benchmark(part_one, data)
```

### Dynamic Test Fixture

The `example` fixture automatically:

- Extracts day number from test filename (e.g., `test_day01.py` → day 01)
- Loads corresponding example from `{year}/data/examples/{day}.txt`
- Works across multiple years without changes

## Tips & Best Practices

- **Year organization**: Solutions are organized by year in separate folders. Change year in `.aoc-cli.json`
- **Dynamic tests**: Add example data to `{year}/data/examples/<day>.txt` - tests auto-load it
- **Test imports**: Tests use year-relative imports (`from solutions.dayXX`) - sys.path is set up automatically
- **Read puzzles**: Use `python main.py read <day>` to view puzzles while coding
- **Incremental development**: Scaffold → implement → test → refine
- **Benchmarks**: Use `@pytest.mark.benchmark` tests to track performance
- **Version control**: Commit solutions without `data/inputs/` (contains personal input data)

## Troubleshooting

### aoc-cli not found

```bash
cargo install aoc-cli
```

### Session cookie expired

```bash
aoc credentials -s <new_session_cookie>
```

### Python version mismatch

This project requires Python 3.14+. Check your version:

```bash
python --version
```

### Dependencies issues

```bash
uv sync --refresh
```

## Project Configuration

- **Python version**: 3.14+ (configured in `.python-version`)
- **Package manager**: UV with `pyproject.toml`
- **Linting**: Ruff (PEP 8, F-strings, imports)
- **Testing**: pytest with benchmark plugin
- **Download tool**: aoc-cli (configured in `.aoc-cli.json`)

Happy coding! 🎄
