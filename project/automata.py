__all__ = [
    "regex_to_min_dfa",
    "graph_to_epsilon_nfa",
]

from typing import Set, Optional

from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    EpsilonNFA,
    State,
    Epsilon,
)
from pyformlang.regular_expression import Regex
from pyformlang.regular_expression.regex_objects import Symbol


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
    start_states:
        Set of start states in NFA
        If parameter is None then each graph node is considered the start state
    final_states:
        Set of final states in NFA
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
            symb_by=Symbol(data.get("label", Epsilon)),
        )

    set_of_all_nodes = set(graph.nodes)

    if start_states is None:
        start_states = set_of_all_nodes
    for state in start_states:
        epsilon_nfa.add_start_state(state)

    if final_states is None:
        final_states = set_of_all_nodes
    for state in final_states:
        epsilon_nfa.add_final_state(state)

    return epsilon_nfa
