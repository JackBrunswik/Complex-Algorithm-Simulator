import random
import networkx as nx
from collections import deque

class RandomGraphBFS:
    """ Random Graph BFS Simulation:
    Generates a connected random graph and performs BFS traversal.
    Designed for both Monte Carlo statistical experiments and real-time visualization. """

    def __init__(self, p=0.1):
        self.p = p

    # Graph generation
    def generate_connected_graph(self, n):
        # Generates a connected random graph G(n, p)
        while True:
            G = nx.erdos_renyi_graph(n, self.p)
            if nx.is_connected(G):
                return G

    # BFS execution
    def run_bfs(self, G, start_node=0):
        # Runs BFS on graph G starting from start_node
        visited = set()
        queue = deque()
        levels = {}

        edges_examined = 0

        visited.add(start_node)
        queue.append(start_node)
        levels[start_node] = 0

        while queue:

            current = queue.popleft()

            for neighbor in G.neighbors(current):

                edges_examined += 1  # Count every edge check

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    levels[neighbor] = levels[current] + 1

        tree_height = max(levels.values())

        return {
            "edges_examined": edges_examined,
            "nodes_visited": len(visited),
            "tree_height": tree_height
        }