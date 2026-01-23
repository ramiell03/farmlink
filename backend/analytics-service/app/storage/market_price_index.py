from typing import Dict, List
from app.algorithms.segment_tree import SegmentTree

def avg_merge(a: float, b: float) -> float:
    return a + b


class MarketPriceIndex:
    def __init__(self):
        self.prices: Dict[str, List[float]] = {}
        self.quantities: Dict[str, List[int]] = {}
        self.trees: Dict[str, SegmentTree] = {}

    def add_price(self, crop: str, price: float, quantity: int):
        if crop not in self.prices:
            self.prices[crop] = []
            self.quantities[crop] = []
            self.trees[crop] = SegmentTree([], avg_merge)

        self.prices[crop].append(price)
        self.quantities[crop].append(quantity)
        self.trees[crop] = SegmentTree(self.prices[crop], avg_merge)

    def latest_price(self, crop: str) -> float:
        if crop not in self.prices or not self.prices[crop]:
            return 0.0
        return self.prices[crop][-1]

    def total_quantity(self, crop: str) -> int:
        return sum(self.quantities.get(crop, []))

    def listings_count(self, crop: str) -> int:
        return len(self.prices.get(crop, []))

