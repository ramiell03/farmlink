from collections import defaultdict

class AggregationService:
    """
    In-memory aggregation helper (used by background jobs)
    """

    def __init__(self):
        # ---- MARKET DATA ----
        self.crop_prices = defaultdict(list)
        self.crop_quantity = defaultdict(int)
        self.crop_listings = defaultdict(int)

        # ---- DEMAND ----
        self.crop_demand = defaultdict(int)

        # ---- FARMER PERFORMANCE ----
        self.farmer_sales = defaultdict(int)

    # -------- PRICE / SUPPLY --------
    def record_price(self, crop: str, price: float, quantity: int):
        self.crop_prices[crop].append(price)
        self.crop_quantity[crop] += quantity
        self.crop_listings[crop] += 1

    def average_price(self, crop: str) -> float:
        prices = self.crop_prices[crop]
        return sum(prices) / len(prices) if prices else 0.0

    def total_quantity(self, crop: str) -> int:
        return self.crop_quantity[crop]

    def listings_count(self, crop: str) -> int:
        return self.crop_listings[crop]

    # -------- DEMAND --------
    def record_demand(self, crop: str, quantity: int):
        self.crop_demand[crop] += quantity

    def demand_index(self, crop: str) -> float:
        return min(self.crop_demand[crop] / 1000, 1.0)

    # -------- FARMER PERFORMANCE --------
    def record_sale(self, farmer_id: str, quantity: int):
        self.farmer_sales[farmer_id] += quantity

    def farmer_reliability(self, farmer_id: str) -> float:
        return min(self.farmer_sales[farmer_id] / 500, 1.0)


aggregation_service = AggregationService()
