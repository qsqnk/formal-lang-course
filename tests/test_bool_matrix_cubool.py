import pytest
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol

from tests.utils import *

if system_is_linux():
    from project.matrix_utils_pycubool import *


@pytest.fixture
def empty_nfa():
    return EpsilonNFA()


@pytest.fixture
def non_empty_nfa():
    nfa = EpsilonNFA()
    nfa.add_transition(State(0), Symbol("a"), State(0))
    nfa.add_transition(State(0), Symbol("b"), State(1))
    nfa.add_transition(State(1), Symbol("c"), State(1))
    nfa.add_start_state(State(0))
    nfa.add_final_state(State(1))
    return nfa


def test_bool_matrix_from_empty_nfa(empty_nfa):
    if not system_is_linux():
        return
    mtx = BoolMatrixAutomatonPyCuBool.from_nfa(empty_nfa)
    assert all(
        (
            not mtx.start_states,
            not mtx.final_states,
            not mtx.state_to_idx,
            not mtx.b_mtx,
        )
    )


def test_bool_matrix_from_non_empty_nfa_states(non_empty_nfa):
    if not system_is_linux():
        return
    mtx = BoolMatrixAutomatonPyCuBool.from_nfa(non_empty_nfa)
    assert all(
        (
            {State(0)} == mtx.start_states,
            {State(1)} == mtx.final_states,
            {State(0): 0, State(1): 1} == mtx.state_to_idx,
        )
    )


def test_bool_matrix_from_non_empty_nfa_matrix(non_empty_nfa):
    if not system_is_linux():
        return
    mtx = BoolMatrixAutomatonPyCuBool.from_nfa(non_empty_nfa)
    assert all(
        (
            [(0, 0)] == mtx.b_mtx["a"].to_list(),
            [(0, 1)] == mtx.b_mtx["b"].to_list(),
            [(1, 1)] == mtx.b_mtx["c"].to_list(),
        )
    )


def test_bool_matrix_intersection_with_empty(non_empty_nfa, empty_nfa):
    if not system_is_linux():
        return
    intersection = BoolMatrixAutomatonPyCuBool.from_nfa(
        non_empty_nfa
    ) & BoolMatrixAutomatonPyCuBool.from_nfa(empty_nfa)
    assert all(
        (
            not intersection.start_states,
            not intersection.final_states,
            not intersection.state_to_idx,
            not intersection.b_mtx,
        )
    )


def test_intersection_with_non_empty_automaton_states(non_empty_nfa):
    if not system_is_linux():
        return
    intersection = BoolMatrixAutomatonPyCuBool.from_nfa(
        non_empty_nfa
    ) & BoolMatrixAutomatonPyCuBool.from_nfa(non_empty_nfa)
    assert all(
        (
            {State((0, 0))} == intersection.start_states,
            {State((1, 1))} == intersection.final_states,
            {State((0, 0)): 0, State((0, 1)): 1, State((1, 0)): 2, State((1, 1)): 3}
            == intersection.state_to_idx,
        )
    )


def test_intersection_with_non_empty_automaton_matrix(non_empty_nfa):
    if not system_is_linux():
        return
    intersection = BoolMatrixAutomatonPyCuBool.from_nfa(
        non_empty_nfa
    ) & BoolMatrixAutomatonPyCuBool.from_nfa(non_empty_nfa)
    assert all(
        (
            [(0, 0)] == intersection.b_mtx["a"].to_list(),
            [(0, 3)] == intersection.b_mtx["b"].to_list(),
            [(3, 3)] == intersection.b_mtx["c"].to_list(),
        )
    )


def test_transitive_closure_empty(empty_nfa):
    if not system_is_linux():
        return
    tc = BoolMatrixAutomatonPyCuBool.from_nfa(empty_nfa).transitive_closure()
    assert not tc.to_list()


def test_transitive_closure_non_empty(non_empty_nfa):
    if not system_is_linux():
        return
    tc = BoolMatrixAutomatonPyCuBool.from_nfa(non_empty_nfa).transitive_closure()
    assert [(0, 0), (0, 1), (1, 1)] == tc.to_list()
