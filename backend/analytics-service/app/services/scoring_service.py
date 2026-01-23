
def farmer_score(price: float, quantity: int, rating: float = 3.0) -> float:
    price_score = 1 / max(price, 1)
    quantity_score = min(quantity / 100, 1)
    rating_score = min(rating / 5, 1)

    return round(
        price_score * 0.4 +
        quantity_score * 0.35 +
        rating_score * 0.25,
        3
    )
