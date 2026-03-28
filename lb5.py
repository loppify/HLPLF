import networkx as nx
import matplotlib.pyplot as plt


def read_graph_from_file(filename, directed=True):
    """
    Зчитує граф з файлу.
    Формат:
    u v

    >>> data = "1 2\\n2 3\\n3 1\\n"
    >>> with open("test.txt", "w") as f:
    ...     _ = f.write(data)
    >>> G = read_graph_from_file("test.txt")
    >>> sorted(G.edges())
    [(1, 2), (2, 3), (3, 1)]

    >>> data = "1 2\\n2 4\\n"
    >>> with open("test2.txt", "w") as f:
    ...     _ = f.write(data)
    >>> G2 = read_graph_from_file("test2.txt")
    >>> sorted(G2.edges())
    [(1, 2), (2, 4)]
    """

    G = nx.DiGraph() if directed else nx.Graph()

    with open(filename, "r") as f:
        for line in f:
            u, v = map(int, line.split())
            G.add_edge(u, v)

    return G


def draw_graph(G):
    """
    Малює граф.

    >>> G = nx.DiGraph()
    >>> G.add_edge(1, 2)
    >>> draw_graph(G)  # doctest: +SKIP
    """
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True)
    plt.show()


def shortest_path_between(G, X, Y):
    """
    Повертає мінімальний шлях між X та Y.

    >>> G = nx.DiGraph()
    >>> G.add_edges_from([(1,2), (2,3), (1,3)])
    >>> shortest_path_between(G, 1, 3)
    [1, 3]

    >>> G2 = nx.DiGraph()
    >>> G2.add_edges_from([(1,2), (2,3)])
    >>> shortest_path_between(G2, 1, 3)
    [1, 2, 3]
    """

    try:
        return nx.shortest_path(G, X, Y)
    except nx.NetworkXNoPath:
        return []


def longest_cycle_containing_vertex(G, v):
    """
    Повертає найдовший цикл, що містить вершину v.

    >>> G = nx.DiGraph()
    >>> G.add_edges_from([(1,2),(2,3),(3,1),(2,4)])
    >>> sorted(longest_cycle_containing_vertex(G, 1))
    [1, 2, 3]

    >>> G2 = nx.DiGraph()
    >>> G2.add_edges_from([(1,2),(2,3)])
    >>> longest_cycle_containing_vertex(G2, 1)
    []
    """

    cycles = list(nx.simple_cycles(G))
    max_cycle = []

    for cycle in cycles:
        if v in cycle and len(cycle) > len(max_cycle):
            max_cycle = cycle

    return max_cycle


__all__ = [
    "read_graph_from_file",
    "draw_graph",
    "shortest_path_between",
    "longest_cycle_containing_vertex"
]
if __name__ == "__main__":
    import doctest

    print("Running doctests...")
    doctest.testmod(verbose=True)

    print("\nDrawing test graph...")

    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1), (2, 4)])

    draw_graph(G)
