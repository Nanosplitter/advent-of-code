"""
Advent of Code Runner Module
============================

This module provides utilities to easily run AoC solutions with different input files.

Usage in your solution.py:
    from libraries.aoc_runner import run, get_input

    def part1(data):
        # your solution
        return result

    def part2(data):
        # your solution
        return result

    if __name__ == "__main__":
        run(part1, part2)

Or manually get input:
    data = get_input()  # Reads based on INPUT_TYPE env var or --input arg
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Callable, Any, Optional


# ANSI color codes for pretty output
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


INPUT_FILES = {
    "input": "input.txt",
    "example": "ex_input.txt",
    "simple": "simple_input.txt",
    "ex": "ex_input.txt",  # alias
    "i": "input.txt",  # alias
    "e": "ex_input.txt",  # alias
    "s": "simple_input.txt",  # alias
}


def get_solution_dir() -> Path:
    """Get the directory of the calling solution file."""
    # Walk up the stack to find the solution.py file
    import inspect

    for frame_info in inspect.stack():
        filepath = Path(frame_info.filename)
        if filepath.name == "solution.py":
            return filepath.parent
    # Fallback to current working directory
    return Path.cwd()


def get_input_type() -> str:
    """
    Determine which input file to use.
    Priority:
    1. Command line argument: --input <type>
    2. Environment variable: INPUT_TYPE
    3. Default: "input"
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--input",
        "-i",
        dest="input_type",
        choices=list(INPUT_FILES.keys()),
        help="Input file type to use",
    )
    parser.add_argument(
        "--part",
        "-p",
        dest="part",
        type=int,
        choices=[1, 2],
        help="Run only part 1 or 2",
    )
    args, _ = parser.parse_known_args()

    if args.input_type:
        return args.input_type

    env_type = os.environ.get("INPUT_TYPE", "input").lower()
    return env_type if env_type in INPUT_FILES else "input"


def get_part_filter() -> Optional[int]:
    """Get which part to run (1, 2, or None for both)."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--part", "-p", dest="part", type=int, choices=[1, 2])
    args, _ = parser.parse_known_args()

    if args.part:
        return args.part

    env_part = os.environ.get("AOC_PART", "")
    if env_part in ("1", "2"):
        return int(env_part)
    return None


def get_input(
    input_type: Optional[str] = None, solution_dir: Optional[Path] = None
) -> list[str]:
    """
    Read the input file and return lines.

    Args:
        input_type: Override the input type (input, example, simple)
        solution_dir: Override the solution directory

    Returns:
        List of lines from the input file (with newlines stripped)
    """
    if input_type is None:
        input_type = get_input_type()

    if solution_dir is None:
        solution_dir = get_solution_dir()

    filename = INPUT_FILES.get(input_type, "input.txt")
    filepath = solution_dir / filename

    if not filepath.exists():
        print(f"{Colors.RED}Error: Input file not found: {filepath}{Colors.ENDC}")
        sys.exit(1)

    with open(filepath, "r") as f:
        return f.read().splitlines()


def get_input_raw(
    input_type: Optional[str] = None, solution_dir: Optional[Path] = None
) -> str:
    """
    Read the input file and return raw content.

    Returns:
        Raw string content of the input file
    """
    if input_type is None:
        input_type = get_input_type()

    if solution_dir is None:
        solution_dir = get_solution_dir()

    filename = INPUT_FILES.get(input_type, "input.txt")
    filepath = solution_dir / filename

    if not filepath.exists():
        print(f"{Colors.RED}Error: Input file not found: {filepath}{Colors.ENDC}")
        sys.exit(1)

    with open(filepath, "r") as f:
        return f.read()


def run(
    part1: Callable[[Any], Any],
    part2: Optional[Callable[[Any], Any]] = None,
    parser: Optional[Callable[[list[str]], Any]] = None,
) -> None:
    """
    Run the solution with the selected input.

    Args:
        part1: Function for part 1 solution
        part2: Function for part 2 solution (optional)
        parser: Function to parse input lines into desired format (optional)
                If not provided, raw lines are passed to part functions
    """
    input_type = get_input_type()
    part_filter = get_part_filter()
    solution_dir = get_solution_dir()

    # Pretty header
    day_match = None
    for parent in solution_dir.parts:
        if parent.startswith("day"):
            day_match = parent
            break

    day_str = day_match or solution_dir.name
    input_display = INPUT_FILES.get(input_type, input_type)

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 50}{Colors.ENDC}")
    print(
        f"{Colors.BOLD}{Colors.CYAN}🎄 Advent of Code - {day_str.upper()} 🎄{Colors.ENDC}"
    )
    print(f"{Colors.YELLOW}   Input: {input_display}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'=' * 50}{Colors.ENDC}\n")

    # Read and parse input
    lines = get_input(input_type, solution_dir)
    data = parser(lines) if parser else lines

    def run_part(part_num: int, func: Callable, data: Any) -> None:
        if func is None:
            return
        if part_filter is not None and part_filter != part_num:
            return

        print(f"{Colors.BLUE}▶ Part {part_num}:{Colors.ENDC}")
        start = time.perf_counter()
        try:
            result = func(data)
            elapsed = time.perf_counter() - start
            print(f"  {Colors.GREEN}{Colors.BOLD}Result: {result}{Colors.ENDC}")
            print(f"  {Colors.HEADER}Time: {elapsed * 1000:.2f}ms{Colors.ENDC}\n")
        except Exception as e:
            elapsed = time.perf_counter() - start
            print(f"  {Colors.RED}Error: {e}{Colors.ENDC}")
            print(f"  {Colors.HEADER}Time: {elapsed * 1000:.2f}ms{Colors.ENDC}\n")
            raise

    run_part(1, part1, data)
    run_part(2, part2, data)

    print(f"{Colors.CYAN}{'=' * 50}{Colors.ENDC}\n")


# Quick access functions for common parsing patterns
def parse_ints(lines: list[str]) -> list[int]:
    """Parse each line as an integer."""
    return [int(line) for line in lines if line.strip()]


def parse_grid(lines: list[str]) -> list[list[str]]:
    """Parse input as a 2D character grid."""
    return [list(line) for line in lines]


def parse_int_grid(lines: list[str]) -> list[list[int]]:
    """Parse input as a 2D integer grid."""
    return [[int(c) for c in line] for line in lines]


if __name__ == "__main__":
    # Test the module
    print("AOC Runner Module")
    print(f"Input type: {get_input_type()}")
    print(f"Part filter: {get_part_filter()}")
