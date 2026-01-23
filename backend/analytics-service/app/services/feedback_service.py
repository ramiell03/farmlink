from app.storage.market_price_index import price_index
from app.storage.cache import cache_delete

def record_order_feedback(
    crop: str,
    price: float,
    quantity: int
):
    """
    Learn from confirmed orders
    """

    # Update price index (segment tree)
    price_index.add_price(crop, price)

    # Invalidate related caches
    cache_delete(f"prediction:{crop}")
    cache_delete(f"insights:{crop}")
    cache_delete(f"match:farmers:{crop}")
