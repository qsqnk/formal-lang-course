from typing import NamedTuple, Set, Tuple, Union

import cfpq_data
import networkx.drawing.nx_pydot
from networkx import MultiDiGraph

__all__ = [
    'GraphInfo',
    'graph_info_of',
    'build_two_cycle_labeled_graph',
    'load_graph',
    'save_graph'
]

from typing.io import IO


class GraphInfo(NamedTuple):
    number_of_nodes: int
    number_of_edges: int
    edge_labels: Set[str]


def graph_info_of(graph: MultiDiGraph) -> GraphInfo:
    edge_labels = set(
        label for _, _, label in graph.edges(data='label') if label
    )
    return GraphInfo(
        number_of_nodes=graph.number_of_nodes(),
        number_of_edges=graph.number_of_edges(),
        edge_labels=edge_labels,
    )


def build_two_cycle_labeled_graph(
        size_of_first_cycle: int,
        size_of_second_cycle: int,
        edge_labels: Tuple[str, str],
) -> MultiDiGraph:
    return cfpq_data.labeled_two_cycles_graph(
        n=size_of_first_cycle,
        m=size_of_second_cycle,
        labels=edge_labels,
    )


def load_graph(graph_name: str) -> MultiDiGraph:
    graph_path = cfpq_data.download(graph_name)
    return cfpq_data.graph_from_csv(graph_path)


def save_graph(graph: MultiDiGraph, file: Union[str, IO]) -> None:
    networkx.drawing.nx_pydot.write_dot(graph, file)
