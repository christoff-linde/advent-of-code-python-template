"""AOC CLI integration for downloading inputs and puzzles."""

import subprocess
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_aoc_data_dir(year: int | None = None) -> Path:
    """Get the data directory path.

    Args:
        year: Optional year number. If provided, returns year-specific data dir.
              If None, returns root data directory.

    Returns:
        Path to the data directory (year-specific or root).
    """
    root = get_project_root()
    if year is None:
        return root / "data"
    return root / str(year) / "data"


def check_aoc_cli() -> bool:
    """Check if aoc-cli is installed."""
    try:
        subprocess.run(["aoc", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_input(day: int, year: int) -> Path:
    """
    Download input for a specific day using aoc-cli.

    Args:
        day: Day number (1-25)
        year: Year

    Returns:
        Path to the downloaded input file
    """
    if not check_aoc_cli():
        raise RuntimeError(
            "aoc-cli not found. Install it with: cargo install aoc-cli\n"
            "Then configure with: aoc credentials -s <session_cookie>"
        )

    data_dir = get_aoc_data_dir(year)
    data_dir.parent.mkdir(parents=True, exist_ok=True)
    input_file = data_dir / "inputs" / f"{day:02d}.txt"
    input_file.parent.mkdir(parents=True, exist_ok=True)

    # Use aoc-cli to download - run from project root
    try:
        result = subprocess.run(
            [
                "aoc",
                "download",
                "--year",
                str(year),
                "--day",
                str(day),
                "--input-only",
                "--input-file",
                str(input_file),
                "--overwrite",
            ],
            cwd=get_project_root(),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Failed to download input: {result.stderr}")

        # Verify file was created
        if not input_file.exists():
            raise RuntimeError(
                f"Download succeeded but file not found at {input_file}\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )

        return input_file
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to download input: {e.stderr}")


def download_puzzle(day: int, year: int) -> Path:
    """
    Download puzzle description for a specific day using aoc-cli.

    Args:
        day: Day number (1-25)
        year: Year

    Returns:
        Path to the downloaded puzzle file
    """
    if not check_aoc_cli():
        raise RuntimeError(
            "aoc-cli not found. Install it with: cargo install aoc-cli\n"
            "Then configure with: aoc credentials -s <session_cookie>"
        )

    data_dir = get_aoc_data_dir(year)
    data_dir.parent.mkdir(parents=True, exist_ok=True)
    puzzle_file = data_dir / "puzzles" / f"{day:02d}.md"
    puzzle_file.parent.mkdir(parents=True, exist_ok=True)

    # Use aoc-cli to download - run from project root
    try:
        result = subprocess.run(
            [
                "aoc",
                "download",
                "--year",
                str(year),
                "--day",
                str(day),
                "--puzzle-only",
                "--puzzle-file",
                str(puzzle_file),
                "--overwrite",
            ],
            cwd=get_project_root(),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Failed to download puzzle: {result.stderr}")

        # Verify file was created
        if not puzzle_file.exists():
            raise RuntimeError(
                f"Download succeeded but file not found at {puzzle_file}\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )

        return puzzle_file
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to download puzzle: {e.stderr}")


def read_input(day: int, year: int | None = None) -> str:
    """Read input file for a specific day.

    Args:
        day: Day number (1-25)
        year: Optional year. If not provided, uses root data directory.

    Returns:
        Contents of the input file
    """
    data_dir = get_aoc_data_dir(year)
    input_file = data_dir / "inputs" / f"{day:02d}.txt"

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}\n"
            f"Download it with: python main.py download {day}"
        )

    return input_file.read_text()


def read_example(day: int, year: int | None = None) -> str:
    """Read example file for a specific day.

    Args:
        day: Day number (1-25)
        year: Optional year. If not provided, uses root data directory.

    Returns:
        Contents of the example file
    """
    data_dir = get_aoc_data_dir(year)
    example_file = data_dir / "examples" / f"{day:02d}.txt"

    if not example_file.exists():
        raise FileNotFoundError(f"Example file not found: {example_file}")

    return example_file.read_text()


def read_puzzle(day: int, year: int | None = None) -> str:
    """Read puzzle description for a specific day.

    Args:
        day: Day number (1-25)
        year: Optional year. If not provided, uses root data directory.

    Returns:
        Contents of the puzzle file
    """
    data_dir = get_aoc_data_dir(year)
    puzzle_file = data_dir / "puzzles" / f"{day:02d}.md"

    if not puzzle_file.exists():
        raise FileNotFoundError(
            f"Puzzle file not found: {puzzle_file}\n"
            f"Download it with: python main.py download {day}"
        )

    return puzzle_file.read_text()
