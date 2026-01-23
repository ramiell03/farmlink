from typing import Dict, List, Tuple
import heapq

class Graph:
    """
    Weighted graph using adjacency list
    """

    def __init__(self):
        self.adjacency: Dict[str, List[Tuple[str, float]]] = {}

    def add_node(self, node_id: str):
        if node_id not in self.adjacency:
            self.adjacency[node_id] = []

    def add_edge(self, from_node: str, to_node: str, weight: float):
        self.add_node(from_node)
        self.add_node(to_node)
        self.adjacency[from_node].append((to_node, weight))
        self.adjacency[to_node].append((from_node, weight))  # undirected

    def neighbors(self, node_id: str):
        return self.adjacency.get(node_id, [])

    def shortest_path(self, start: str) -> Dict[str, float]:
        """
        Dijkstra: shortest distance from start to all nodes
        """
        distances = {node: float("inf") for node in self.adjacency}
        distances[start] = 0.0

        pq = [(0.0, start)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_dist > distances[current_node]:
                continue

            for neighbor, weight in self.adjacency[current_node]:
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances
