from typing import List, Callable
from dataclasses import dataclass

@dataclass
class SegmentNode:
    left: int
    right: int
    value: float = 0.0


class SegmentTree:
    """
    Segment Tree for range queries (sum, min, max, avg).
    """

    def __init__(self, data: List[float], merge_fn: Callable):
        self.n = len(data)
        self.data = data
        self.merge = merge_fn
        self.tree = [None] * (4 * self.n)
        if self.n > 0:
            self._build(1, 0, self.n - 1)

    def _build(self, index: int, left: int, right: int):
        if left == right:
            self.tree[index] = SegmentNode(left, right, self.data[left])
            return

        mid = (left + right) // 2
        self._build(index * 2, left, mid)
        self._build(index * 2 + 1, mid + 1, right)

        self.tree[index] = SegmentNode(
            left,
            right,
            self.merge(
                self.tree[index * 2].value,
                self.tree[index * 2 + 1].value
            )
        )

    def query(self, ql: int, qr: int) -> float:
        return self._query(1, ql, qr)

    def _query(self, index: int, ql: int, qr: int) -> float:
        node = self.tree[index]

        if node.left > qr or node.right < ql:
            return 0.0

        if ql <= node.left and node.right <= qr:
            return node.value

        return self.merge(
            self._query(index * 2, ql, qr),
            self._query(index * 2 + 1, ql, qr)
        )

    def update(self, pos: int, value: float):
        self._update(1, pos, value)

    def _update(self, index: int, pos: int, value: float):
        node = self.tree[index]

        if node.left == node.right:
            node.value = value
            return

        mid = (node.left + node.right) // 2

        if pos <= mid:
            self._update(index * 2, pos, value)
        else:
            self._update(index * 2 + 1, pos, value)

        node.value = self.merge(
            self.tree[index * 2].value,
            self.tree[index * 2 + 1].value
        )
