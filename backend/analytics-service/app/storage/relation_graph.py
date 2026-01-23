from app.algorithms.graph import Graph

class MarketRelationshipGraph:
    """
    Maintains relationships between farmers, buyers, and markets
    """

    def __init__(self):
        self.graph = Graph()

    def connect_farmer_market(self, farmer_id: str, market_id: str, distance: float):
        self.graph.add_edge(f"farmer:{farmer_id}", f"market:{market_id}", distance)

    def connect_buyer_market(self, buyer_id: str, market_id: str, distance: float):
        self.graph.add_edge(f"buyer:{buyer_id}", f"market:{market_id}", distance)

    def record_trade(self, farmer_id: str, buyer_id: str, strength: float):
        """
        Lower weight = stronger relationship
        """
        self.graph.add_edge(
            f"farmer:{farmer_id}",
            f"buyer:{buyer_id}",
            1 / max(strength, 0.1)
        )

    def nearest_partners(self, node_id: str, top_k: int = 5):
        distances = self.graph.shortest_path(node_id)
        return sorted(distances.items(), key=lambda x: x[1])[:top_k]
