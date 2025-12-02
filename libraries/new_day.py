"""
New Day Setup Script for Advent of Code
========================================

Creates a new day folder with template files.

Usage:
    python libraries/new_day.py           # Auto-detects next day
    python libraries/new_day.py 5         # Creates day 5
    python libraries/new_day.py 2024 5    # Creates day 5 in 2024
"""

import sys
from datetime import datetime
from pathlib import Path

TEMPLATE = '''"""
Advent of Code {year} - Day {day}
"""
import sys
sys.path.insert(0, str(__file__).split('{year}')[0])
from libraries.aoc_runner import run, get_input


def parse(lines: list[str]):
    """Parse the input lines into your desired format."""
    # Common patterns:
    # return lines                           # Raw lines
    # return [int(x) for x in lines]         # List of integers
    # return [list(x) for x in lines]        # 2D character grid
    # return lines[0].split(',')             # Comma-separated first line
    return lines


def part1(data) -> int:
    """Solve part 1."""
    return 0


def part2(data) -> int:
    """Solve part 2."""
    return 0


if __name__ == "__main__":
    run(part1, part2, parser=parse)
'''


def get_workspace_root() -> Path:
    """Get the workspace root directory."""
    # Try to find the root by looking for common markers
    current = Path(__file__).resolve()
    while current.parent != current:
        if (current / ".git").exists() or (current / "libraries").exists():
            return current
        current = current.parent
    return Path.cwd()


def find_next_day(year_folder: Path) -> int:
    """Find the next day number to create."""
    existing_days = []
    if year_folder.exists():
        for item in year_folder.iterdir():
            if item.is_dir() and item.name.startswith("day"):
                try:
                    day_num = int(item.name.replace("day", "").lstrip("0") or "0")
                    existing_days.append(day_num)
                except ValueError:
                    pass

    if not existing_days:
        return 1
    return max(existing_days) + 1


def create_day(year: int, day: int, workspace_root: Path) -> None:
    """Create a new day folder with template files."""
    year_folder = workspace_root / str(year)
    day_folder = year_folder / f"day{day:02d}"

    if day_folder.exists():
        print(f"⚠️  Day folder already exists: {day_folder}")
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != "y":
            print("Aborted.")
            return

    # Create folder
    day_folder.mkdir(parents=True, exist_ok=True)

    # Create input files
    input_files = ["input.txt", "ex_input.txt", "simple_input.txt"]
    for filename in input_files:
        filepath = day_folder / filename
        if not filepath.exists():
            filepath.touch()
            print(f"  📄 Created {filename}")

    # Create solution file
    solution_path = day_folder / "solution.py"
    solution_content = TEMPLATE.format(year=year, day=day)
    solution_path.write_text(solution_content)
    print("  🐍 Created solution.py")

    print(f"\n✅ Created {year}/day{day:02d}/")
    print(f"   📂 {day_folder}")


def main():
    workspace_root = get_workspace_root()
    current_year = datetime.now().year

    args = sys.argv[1:]

    if len(args) == 0:
        # Auto-detect: current year, next day
        year = current_year
        year_folder = workspace_root / str(year)
        day = find_next_day(year_folder)
    elif len(args) == 1:
        # One arg: could be day number for current year
        year = current_year
        day = int(args[0])
    elif len(args) == 2:
        # Two args: year and day
        year = int(args[0])
        day = int(args[1])
    else:
        print("Usage: python new_day.py [day] or python new_day.py [year] [day]")
        sys.exit(1)

    if day < 1 or day > 25:
        print(f"⚠️  Day must be between 1 and 25, got: {day}")
        sys.exit(1)

    print("\n🎄 Advent of Code - New Day Setup 🎄")
    print(f"   Year: {year}")
    print(f"   Day:  {day}\n")

    create_day(year, day, workspace_root)


if __name__ == "__main__":
    main()
