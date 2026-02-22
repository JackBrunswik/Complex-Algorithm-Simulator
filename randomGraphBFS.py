import random
import networkx as nx
from collections import deque

class RandomGraphBFS:
    """ Random Graph BFS Simulation:
    Generates a connected random graph and performs BFS traversal.
    Designed for both Monte Carlo statistical experiments and real-time visualization. """

    def __init__(self, p=0.1):

        self.p = p
        self.reset_metrics()

    # Metrics
    def reset_metrics(self):
        self.nodes_visited = 0
        self.edges_examined = 0

    # Graph Generation
    def generate_connected_graph(self, n):

        G = nx.Graph()
        G.add_nodes_from(range(n))

        # Step 1: Random spanning tree
        nodes = list(range(n))
        random.shuffle(nodes)

        for i in range(1, n):
            parent = random.choice(nodes[:i])
            G.add_edge(nodes[i], parent)

        # Step 2: Add extra random edges
        for i in range(n):
            for j in range(i + 1, n):
                if not G.has_edge(i, j):
                    if random.random() < self.p:
                        G.add_edge(i, j)

        return G

    # BFS Algorithm
    def bfs(self, G, start=0):

        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            self.nodes_visited += 1

            for neighbor in G.neighbors(node):
                self.edges_examined += 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    # Monte Carlo Run Interface
    def run(self, n):

        self.reset_metrics()

        G = self.generate_connected_graph(n)
        self.bfs(G)

        return {
            "nodes_visited": self.nodes_visited,
            "edges_examined": self.edges_examined,
            "total_edges": G.number_of_edges()
        }