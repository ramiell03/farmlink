from dataclasses import dataclass, field
from typing import Any, List

@dataclass(order=True)
class PriorityItem:
    priority: float
    item: Any = field(compare=False)


class MaxPriorityQueue:
    """
    Max-Heap Priority Queue
    """

    def __init__(self):
        self.heap: List[PriorityItem] = []

    def push(self, priority: float, item: Any):
        self.heap.append(PriorityItem(priority, item))
        self._heapify_up(len(self.heap) - 1)

    def pop(self) -> Any:
        if not self.heap:
            return None

        self._swap(0, len(self.heap) - 1)
        max_item = self.heap.pop()
        self._heapify_down(0)
        return max_item.item

    def peek(self) -> Any:
        return self.heap[0].item if self.heap else None

    def _heapify_up(self, index: int):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index].priority > self.heap[parent].priority:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index: int):
        left = 2 * index + 1
        right = 2 * index + 2
        largest = index

        if left < len(self.heap) and self.heap[left].priority > self.heap[largest].priority:
            largest = left

        if right < len(self.heap) and self.heap[right].priority > self.heap[largest].priority:
            largest = right

        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)

    def _swap(self, i: int, j: int):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def is_empty(self) -> bool:
        return len(self.heap) == 0
