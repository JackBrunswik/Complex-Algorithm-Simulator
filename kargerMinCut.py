import random
import networkx as nx

class KargerMinCut:
    """ Implements Karger's Randomized Min-Cut algorithm. Designed for both Monte Carlo simulation and visualization. """

    def generate_graph(self, n, p=0.4):
        """ Generate a connected random graph. """
        while True:
            G = nx.erdos_renyi_graph(n, p)
            if nx.is_connected(G):
                return G

    def run_karger(self, G):
        """ Runs Karger's algorithm and returns the cut size. """
        G = G.copy()

        while len(G.nodes) > 2:
            u, v = random.choice(list(G.edges))

            # Contract edge
            G = nx.contracted_nodes(G, u, v, self_loops=False)

        # Remaining edges between the two supernodes = min cut
        cut_size = G.number_of_edges()

        return {
            "cut_size": cut_size
        }

    def contraction_generator(self, G):
        """ Generator for visualization. Yields graph state after each contraction. """
        G = G.copy()

        while len(G.nodes) > 2:
            # Choose random edge
            u, v = random.choice(list(G.edges))

            # Yield state BEFORE contraction
            yield G.copy(), (u, v)

            # Contract the edge
            G = nx.contracted_nodes(G, u, v, self_loops=False)

        # Final state
        yield G.copy(), None