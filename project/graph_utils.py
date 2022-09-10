from typing import NamedTuple, Set, Tuple, Union

import cfpq_data
import networkx.drawing.nx_pydot
from networkx import MultiDiGraph
from typing.io import IO

__all__ = [
    "GraphInfo",
    "graph_info_of",
    "build_two_cycle_labeled_graph",
    "load_graph",
    "save_graph",
]


class GraphInfo(NamedTuple):
    """Class represents holder of general information about graph.

    Attributes
    ----------

    number_of_nodes : int
        Number of nodes stored in the graph.
    number_of_edges : int
        Number of edges stored in the graph.
    edge_labels : Set[str]
        All labels of edges.
    """

    number_of_nodes: int
    number_of_edges: int
    edge_labels: Set[str]


def graph_info_of(graph: MultiDiGraph) -> GraphInfo:
    """Calculates information about graph.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to be processed

    Returns
    -------
    graph_info : GraphInfo
        Info about graph
    """
    edge_labels = set(label for _, _, label in graph.edges(data="label") if label)
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
    """Builds labeled graph with two cycles.

    Parameters
    ----------
    size_of_first_cycle : int
        Count of nodes in the first cycle without common node
    size_of_second_cycle : int
        Count of nodes in the second cycle without common node
    edge_labels : Tuple[str, str]
        Edge labels of graph

    Returns
    -------
    graph : MultiDiGraph
        Created graph
    """

    return cfpq_data.labeled_two_cycles_graph(
        n=size_of_first_cycle,
        m=size_of_second_cycle,
        labels=edge_labels,
    )


def load_graph(graph_name: str) -> MultiDiGraph:
    """Loads a graph by name.

    Parameters
    ----------
    graph_name : str
        The name of graph in dataset

    Returns
    -------
    graph : MultiDiGraph
        Loaded graph.
    """
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return graph


def save_graph(graph: MultiDiGraph, file: Union[str, IO]) -> None:
    """Saves a graph into a file.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to be saved
    file : Union[str, IO]
        The name of file or file itself

    Returns
    -------
    None
    """
    networkx.drawing.nx_pydot.write_dot(graph, file)
