from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Shape:
    symbol: str
    color: tuple[int, int, int]

class Tube:
    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        self.shapes: List[Shape] = []

    def is_full(self) -> bool:
        return len(self.shapes) >= self.capacity

    def is_empty(self) -> bool:
        return len(self.shapes) == 0

    def can_add(self, shape: Shape) -> bool:
        return not self.is_full()

    def add(self, shape: Shape) -> bool:
        if self.can_add(shape):
            self.shapes.append(shape)
            return True
        return False

    def pop(self) -> Optional[Shape]:
        if not self.is_empty():
            return self.shapes.pop()
        return None

    def peek(self) -> Optional[Shape]:
        if not self.is_empty():
            return self.shapes[-1]
        return None

    def is_complete(self) -> bool:
        if len(self.shapes) != self.capacity:
            return False
        return all(shape.symbol == self.shapes[0].symbol for shape in self.shapes)
