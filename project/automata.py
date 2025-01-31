from typing import Set, Optional

from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    EpsilonNFA,
    State,
    Epsilon,
    Symbol,
)
from pyformlang.regular_expression import Regex

from project import matrix_utils

__all__ = [
    "regex_to_min_dfa",
    "graph_to_epsilon_nfa",
    "intersect_automatons_kron",
]


def regex_to_min_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    """Converts regex to minimal DFA

    Parameters
    ----------
    regex : Regex
        Regular expression to be converted

    Returns
    -------
    dfa : DeterministicFiniteAutomaton
        Minimal DFA
    """
    return regex.to_epsilon_nfa().minimize()


def graph_to_epsilon_nfa(
    graph: MultiDiGraph,
    start_states: Optional[Set],
    final_states: Optional[Set],
) -> EpsilonNFA:
    """Converts graph to NFA with epsilon transitions

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to be converted
    start_states : Optional[Set]
        Set of nodes of the graph that will be treated as start states in NFA
        If parameter is None then each graph node is considered the start state
    final_states : Optional[Set]
        Set of nodes of the graph that will be treated as final states in NFA
        If parameter is None then each graph node is considered the final state

    Returns
    -------
    epsilon_nfa : EpsilonNFA
        NFA with epsilon transitions
    """
    epsilon_nfa = EpsilonNFA()
    for node_from, node_to, data in graph.edges(data=True):
        epsilon_nfa.add_transition(
            s_from=State(node_from),
            s_to=State(node_to),
            symb_by=Epsilon() if not data["label"] else Symbol(data["label"]),
        )

    set_of_all_nodes = set(graph.nodes)

    if start_states is None:
        start_states = set_of_all_nodes
    for state in map(State, start_states):
        epsilon_nfa.add_start_state(state)

    if final_states is None:
        final_states = set_of_all_nodes
    for state in map(State, final_states):
        epsilon_nfa.add_final_state(state)

    return epsilon_nfa


def intersect_automatons_kron(
    first_automaton: EpsilonNFA, second_automaton: EpsilonNFA
) -> EpsilonNFA:
    """Calculates intersection of two automatons using Kronecker multiplication of their bool matrices

    Parameters
    ----------
    first_automaton : EpsilonNFA
        First graph
    second_automaton : EpsilonNFA
        Second graph

    Returns
    -------
    intersected_automaton: EpsilonNFA
        Intersection of first_automaton and second_automaton
    """
    first_graph_mtx = matrix_utils.BoolMatrixAutomaton.from_nfa(first_automaton)
    second_graph_mtx = matrix_utils.BoolMatrixAutomaton.from_nfa(second_automaton)
    intersected = first_graph_mtx & second_graph_mtx
    return intersected.to_nfa()
