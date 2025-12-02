"""
Run all AOC inputs side-by-side in the terminal.
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil
import re
import unicodedata

# ANSI code pattern for stripping when calculating visible length
ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def get_terminal_width():
    """Get terminal width, default to 150 if can't detect."""
    return shutil.get_terminal_size((150, 24)).columns


def char_width(char: str) -> int:
    """Get display width of a character (emoji and wide chars = 2)."""
    if len(char) != 1:
        return sum(char_width(c) for c in char)

    # Check for emoji and other wide characters
    cat = unicodedata.category(char)
    east_asian_width = unicodedata.east_asian_width(char)

    # Wide or fullwidth characters
    if east_asian_width in ("W", "F"):
        return 2

    # Most emoji are in 'So' (Symbol, other) category and have width > 0x1F000
    if ord(char) >= 0x1F300:  # Emoji range starts around here
        return 2

    return 1


def visible_len(s: str) -> int:
    """Get visible length of string (excluding ANSI codes, accounting for wide chars)."""
    stripped = ANSI_ESCAPE.sub("", s)
    return sum(char_width(c) for c in stripped)


def run_solution(file_path: str, input_type: str, cwd: str) -> list[str]:
    """Run the solution with given input type and capture output."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(file_path).parents[2])  # workspace root
    env["PYTHONIOENCODING"] = "utf-8"  # Force UTF-8 encoding

    result = subprocess.run(
        [sys.executable, "-u", file_path, "--input", input_type],
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
        encoding="utf-8",
        errors="replace",
    )

    # Combine stdout and stderr, split into lines
    output = result.stdout + result.stderr
    # Filter out empty lines at start/end, keep structure
    lines = output.splitlines()
    # Remove leading/trailing empty lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def truncate_line(line: str, max_width: int) -> str:
    """Truncate a line to max visible width, preserving ANSI codes."""
    if visible_len(line) <= max_width:
        return line

    # Need to truncate - walk through and count visible chars
    result = []
    vis_count = 0
    i = 0
    while i < len(line) and vis_count < max_width - 1:
        # Check for ANSI escape sequence
        match = ANSI_ESCAPE.match(line, i)
        if match:
            result.append(match.group())
            i = match.end()
        else:
            result.append(line[i])
            vis_count += 1
            i += 1

    result.append("…")
    # Add reset code in case we're in the middle of colored text
    result.append("\033[0m")
    return "".join(result)


def pad_line(line: str, width: int) -> str:
    """Pad a line to exact visible width."""
    current_len = visible_len(line)
    if current_len < width:
        return line + " " * (width - current_len)
    return line


def format_columns(
    outputs: dict[str, list[str]], col_width: int
) -> dict[str, list[str]]:
    """Format all outputs to have uniform width and height."""
    max_height = max(len(lines) for lines in outputs.values())

    result = {}
    for name, lines in outputs.items():
        formatted = []
        for line in lines:
            # Truncate if too long, then pad
            truncated = truncate_line(line, col_width)
            padded = pad_line(truncated, col_width)
            formatted.append(padded)

        # Pad with empty lines to match height
        while len(formatted) < max_height:
            formatted.append(" " * col_width)

        result[name] = formatted

    return result


def print_side_by_side(outputs: dict[str, list[str]]):
    """Print multiple outputs side by side."""
    term_width = get_terminal_width()
    num_cols = len(outputs)
    separator = " │ "
    col_width = (term_width - len(separator) * (num_cols - 1)) // num_cols

    # Format all columns
    formatted = format_columns(outputs, col_width)
    max_height = len(next(iter(formatted.values())))

    # Print header
    names = list(outputs.keys())
    header_parts = [name.center(col_width) for name in names]
    print()
    print(separator.join(header_parts))

    # Print separator line
    sep_line = "─" * col_width
    print(("─┼─").join([sep_line] * num_cols))

    # Print rows
    for i in range(max_height):
        row_parts = [formatted[name][i] for name in names]
        print(separator.join(row_parts))

    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_all.py <solution_file>")
        sys.exit(1)

    solution_file = sys.argv[1]
    solution_dir = str(Path(solution_file).parent)

    # Input types to run
    input_types = ["simple", "example", "input"]

    # Run all and collect outputs
    outputs = {}
    for input_type in input_types:
        input_file = Path(solution_dir) / (
            "simple_input.txt"
            if input_type == "simple"
            else "ex_input.txt"
            if input_type == "example"
            else "input.txt"
        )
        if input_file.exists():
            outputs[input_type.upper()] = run_solution(
                solution_file, input_type, solution_dir
            )
        else:
            outputs[input_type.upper()] = [f"(no {input_type} file)"]

    # Print side by side
    print_side_by_side(outputs)


if __name__ == "__main__":
    main()
