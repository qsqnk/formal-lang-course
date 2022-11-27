from collections import defaultdict, deque
from enum import Enum, auto
from typing import Tuple, Set, Any, Union, Collection, Dict, List
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable, Terminal, Production
from scipy.sparse import dok_matrix

from project.graph_utils import load_graph
from project.cfg_utils import cfg_to_wcnf, cfg_from_file

__all__ = [
    "CFPQAlgorithm",
    "cfpq",
]


class CFPQAlgorithm(Enum):
    """Class represents algorithm of CFPQ task

    Values
    ----------

    HELLINGS : CFPQAlgorithm
        Hellings algorithm
    MATRIX : CFPQAlgorithm
        Matrix algorithm that is based on sparse matrix multiplication
    TENSOR: CFPQAlgorithm
        Tensor algorithm that is based on Kronecker product of sparse matrices
    """

    HELLINGS = auto()
    MATRIX = auto()
    TENSOR = auto()


def cfpq(
    algo: CFPQAlgorithm,
    graph: Union[str, MultiDiGraph],
    cfg: Union[str, CFG],
    start_nodes: Set[Any] = None,
    final_nodes: Set[Any] = None,
    start_symbol: Variable = Variable("S"),
) -> Set[Tuple[Any, Any]]:
    """Executes context-free query on graph using Hellings algorithm

    Parameters
      ----------
      algo : CFPQAlgorithm
          The algorithm that will be used for CFPQ
      cfg : CFG
          Path to file containing context-free grammar or Context-free grammar itself

      graph : Union[str, MultiDiGraph]
          Graph name from cfpq-data dataset or Graph itself

      start_nodes: Set[Any]
          Set of start nodes of the graph. If parameter is not specified then all nodes are treated as start

      final_nodes: Set[Any]
          Set of final nodes of the graph. If parameter is not specified then all nodes are treated as final

      start_symbol: Variable
          Non-terminal that will be treated as start symbol in the given grammar

      Returns
      -------
      result: Set[Tuple[Any, Any]]
          Pairs of vertices between which there is a path with specified constraints
    """
    if isinstance(graph, str):
        graph = load_graph(graph)
    if isinstance(cfg, str):
        cfg = cfg_from_file(cfg)
    cfg._start_symbol = start_symbol
    if not start_nodes:
        start_nodes = graph.nodes
    if not final_nodes:
        final_nodes = graph.nodes

    result = {
        CFPQAlgorithm.HELLINGS: _hellings,
        CFPQAlgorithm.MATRIX: _matrix,
        CFPQAlgorithm.TENSOR: _tensor,
    }[algo](cfg, graph)

    return {
        (i, j)
        for (i, n, j) in result
        if start_symbol == n and i in start_nodes and j in final_nodes
    }


def _hellings(cfg: CFG, graph: MultiDiGraph) -> Set[Tuple[Any, Variable, Any]]:
    """Runs Hellings algorithm on given context-free grammar and graph
    in order to get triples, where the first element is the first vertex,
    the second element is a non-terminal, and the third element is the second vertex
    for which there is a path in the graph between these vertices derived from this non-terminal
    from given context-free grammar

      Parameters
      ----------
      cfg : CFG
          Context-free grammar

      graph : MultiDiGraph
          Graph

      Returns
      -------
      result: Set[Tuple[Any, Variable, Any]]
          Triples of vertices between which there is a path with specified constraints
          and a non-terminal from which the path is derived
    """
    n = graph.number_of_nodes()
    if not n:
        return set()

    wcnf = cfg_to_wcnf(cfg)
    eps_nonterm, term_prods, two_nonterm_prods = _convert_wcnf_prods(wcnf.productions)

    by_eps = {(i, n, i) for i in graph.nodes for n in eps_nonterm}
    by_term = {
        (i, n, j)
        for i, j, label in graph.edges(data="label")
        for n, terms in term_prods.items()
        if Terminal(label) in terms
    }

    result = by_eps | by_term
    dq = deque(result.copy())

    while dq:
        i, n1, j = dq.popleft()
        to_add = set()
        for k, n2, l in result:
            if l == i:
                for n, two_nonterms in two_nonterm_prods.items():
                    new = (k, n, j)
                    if (n2, n1) in two_nonterms and new not in result:
                        dq.append(new)
                        to_add.add(new)
            if j == k:
                for n, two_nonterms in two_nonterm_prods.items():
                    new = (i, n, l)
                    if (n1, n2) in two_nonterms and new not in result:
                        dq.append(new)
                        to_add.add(new)
        result |= to_add

    return result


def _matrix(cfg: CFG, graph: MultiDiGraph) -> Set[Tuple[Any, Variable, Any]]:
    """Runs Matrix algorithm on given context-free grammar and graph
    in order to get triples, where the first element is the first vertex,
    the second element is a non-terminal, and the third element is the second vertex
    for which there is a path in the graph between these vertices derived from this non-terminal
    from given context-free grammar

      Parameters
      ----------
      cfg : CFG
          Context-free grammar

      graph : MultiDiGraph
          Graph

      Returns
      -------
      result: Set[Tuple[Any, Variable, Any]]
          Triples of vertices between which there is a path with specified constraints
          and a non-terminal from which the path is derived
    """
    n = graph.number_of_nodes()
    if not n:
        return set()

    nodes = list(graph.nodes)
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}

    wcnf = cfg_to_wcnf(cfg)
    eps_nonterm, term_prods, two_nonterm_prods = _convert_wcnf_prods(wcnf.productions)

    nonterm_to_mtx = {
        nonterm: dok_matrix((n, n), dtype=bool) for nonterm in wcnf.variables
    }

    for i in range(n):
        for nonterm in eps_nonterm:
            nonterm_to_mtx[nonterm][i, i] = True

    for i_node, j_node, label in graph.edges(data="label"):
        i, j = node_to_idx[i_node], node_to_idx[j_node]
        for nonterm in {
            n for n, terms in term_prods.items() if Terminal(label) in terms
        }:
            nonterm_to_mtx[nonterm][i, j] = True

    while True:
        changed = False
        for nonterm, two_nonterms in two_nonterm_prods.items():
            old_nnz = nonterm_to_mtx[nonterm].nnz
            nonterm_to_mtx[nonterm] += sum(
                nonterm_to_mtx[n1] @ nonterm_to_mtx[n2] for n1, n2 in two_nonterms
            )
            changed |= old_nnz != nonterm_to_mtx[nonterm].nnz
        if not changed:
            break

    return set(
        (nodes[i], nonterm, nodes[j])
        for nonterm, mtx in nonterm_to_mtx.items()
        for i, j in zip(*mtx.nonzero())
    )


def _tensor(cfg: CFG, graph: MultiDiGraph) -> Set[Tuple[Any, Variable, Any]]:
    """Runs Tensor algorithm on given context-free grammar and graph
    in order to get triples, where the first element is the first vertex,
    the second element is a non-terminal, and the third element is the second vertex
    for which there is a path in the graph between these vertices derived from this non-terminal
    from given context-free grammar

      Parameters
      ----------
      cfg : CFG
          Context-free grammar

      graph : MultiDiGraph
          Graph

      Returns
      -------
      result: Set[Tuple[Any, Variable, Any]]
          Triples of vertices between which there is a path with specified constraints
          and a non-terminal from which the path is derived
    """
    return


def _convert_wcnf_prods(
    prods: Collection[Production],
) -> Tuple[
    Set[Variable],
    Dict[Variable, Set[Terminal]],
    Dict[Variable, Set[Tuple[Variable, Variable]]],
]:
    """Utility function for converting productions of context-free grammar in WCNF

    Parameters
    ----------
    prods: Collection[Production]
      Productions

    Returns
    ----------
    result: Tuple[
      Set[Variable],
      Dict[Variable, Set[Terminal]],
      Dict[Variable, Set[Tuple[Variable, Variable]]],
    ]
    Triple of set of non-terminals that produces epsilon,
    mapping from non-terminal to terminal that it produces
    mapping from non-terminal to pairs of non-terminals that it produces
    """
    eps_nonterm = set()
    term_prods = defaultdict(set)
    two_nonterm_prods = defaultdict(set)

    for p in prods:
        head, body = p.head, p.body
        body_len = len(body)
        if body_len == 0:
            eps_nonterm.add(head)
        elif body_len == 1:
            term_prods[head].add(body[0])
        elif body_len == 2:
            two_nonterm_prods[head].add((body[0], body[1]))

    return (
        eps_nonterm,
        term_prods,
        two_nonterm_prods,
    )
