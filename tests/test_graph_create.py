import cfpq_data
import networkx

from project.graph_utils import *


def test_create_labeled_two_cycles_graph():
    expected_graph = cfpq_data.labeled_two_cycles_graph(
        n=42,
        m=29,
        labels=("c", "d"),
    )
    actual_graph = build_two_cycle_labeled_graph(
        size_of_first_cycle=42,
        size_of_second_cycle=29,
        edge_labels=("c", "d")
    )
    assert networkx.isomorphism.is_isomorphic(actual_graph, expected_graph)
