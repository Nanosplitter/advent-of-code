from typing import Any


class Grid:
    def __init__(self, items: list[list[Any]]) -> None:
        self.items: list[list[Any]] = items
        self.height: int = len(items)
        self.width: int = len(items[0]) if self.height > 0 else 0

    def get(self, row: int, col: int) -> Any:
        return self.items[row][col]

    def set(self, row: int, col: int, value: Any) -> None:
        self.items[row][col] = value

    def neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        deltas: list[tuple[int, int]] = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        result = []
        for dr, dc in deltas:
            r, c = row + dr, col + dc
            if 0 <= r < self.height and 0 <= c < self.width:
                result.append((self.items[r][c], r, c))
        return result

    def __str__(self) -> str:
        return "\n".join("".join(str(cell) for cell in row) for row in self.items)

    def __repr__(self) -> str:
        return self.__str__()
