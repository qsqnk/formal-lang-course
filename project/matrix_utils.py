__all__ = [
    "BoolMatrix",
]

from typing import Dict, Set, Any

from pyformlang.finite_automaton import State, EpsilonNFA
from scipy.sparse import dok_matrix, kron


class BoolMatrix:
    # Only for internal use
    def __init__(
        self,
        state_to_idx: Dict[State, int],
        start_states: Set[State],
        final_states: Set[State],
        b_mtx: Dict[Any, dok_matrix],
    ):
        self.state_to_idx = state_to_idx
        self.start_states = start_states
        self.final_states = final_states
        self.b_mtx = b_mtx

    def __and__(self, other: "BoolMatrix") -> "BoolMatrix":
        inter_labels = self.b_mtx.keys() & other.b_mtx.keys()
        inter_b_mtx = {
            label: kron(self.b_mtx[label], other.b_mtx[label]) for label in inter_labels
        }
        inter_state_to_idx = dict()
        inter_start_states = set()
        inter_final_states = set()
        for self_state, self_idx in self.state_to_idx.items():
            for other_state, other_idx in other.state_to_idx.items():
                state = State((self_state.value, other_state.value))
                idx = self_idx * len(other.state_to_idx) + other_idx
                inter_state_to_idx[state] = idx
                if (
                    self_state in self.start_states
                    and other_state in other.start_states
                ):
                    inter_start_states.add(state)
                if (
                    self_state in self.final_states
                    and other_state in other.final_states
                ):
                    inter_final_states.add(state)
        return BoolMatrix(
            state_to_idx=inter_state_to_idx,
            start_states=inter_start_states,
            final_states=inter_final_states,
            b_mtx=inter_b_mtx,
        )

    def transitive_closure(self) -> dok_matrix:
        transitive_closure = sum(
            self.b_mtx.values(),
            start=dok_matrix((len(self.state_to_idx), len(self.state_to_idx))),
        )
        prev_nnz, cur_nnz = None, transitive_closure.nnz
        if not cur_nnz:
            return transitive_closure
        while prev_nnz != cur_nnz:
            transitive_closure += transitive_closure @ transitive_closure
            prev_nnz, cur_nnz = cur_nnz, transitive_closure.nnz
        return transitive_closure

    @classmethod
    def from_nfa(cls, nfa: EpsilonNFA) -> "BoolMatrix":
        state_to_idx = {state: idx for idx, state in enumerate(nfa.states)}
        return cls(
            state_to_idx=state_to_idx,
            start_states=nfa.start_states.copy(),
            final_states=nfa.final_states.copy(),
            b_mtx=cls._b_mtx_from_nfa(
                nfa=nfa,
                state_to_idx=state_to_idx,
            ),
        )

    def to_nfa(self) -> EpsilonNFA:
        nfa = EpsilonNFA()
        for label, dok_mtx in self.b_mtx.items():
            mtx_as_arr = dok_mtx.toarray()
            for state_from, i in self.state_to_idx.items():
                for state_to, j in self.state_to_idx.items():
                    if mtx_as_arr[i][j]:
                        nfa.add_transition(
                            s_from=state_from,
                            symb_by=label,
                            s_to=state_to,
                        )
        for state in self.start_states:
            nfa.add_start_state(state)
        for state in self.final_states:
            nfa.add_final_state(state)
        return nfa

    @staticmethod
    def _b_mtx_from_nfa(
        nfa: EpsilonNFA, state_to_idx: Dict[State, int]
    ) -> Dict[Any, dok_matrix]:
        b_mtx = dict()
        state_from_to_transition = nfa.to_dict()
        for label in nfa.symbols:
            dok_mtx = dok_matrix((len(nfa.states), len(nfa.states)), dtype=bool)
            for state_from, transitions in state_from_to_transition.items():
                for state_to in transitions.get(label, {}):
                    dok_mtx[state_to_idx[state_from], state_to_idx[state_to]] = True
            b_mtx[label] = dok_mtx
        return b_mtx
