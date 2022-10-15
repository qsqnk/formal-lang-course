from typing import Dict, Set, Any, List

from pyformlang.finite_automaton import State, EpsilonNFA

from pycubool import Matrix

__all__ = [
    "BoolMatrixAutomatonPyCuBool",
]


class BoolMatrixAutomatonPyCuBool:
    # Only for internal use
    def __init__(
        self,
        state_to_idx: Dict[State, int],
        start_states: Set[State],
        final_states: Set[State],
        b_mtx: Dict[Any, Matrix],
    ):
        """Class represents bool matrix representation of automaton

        Attributes
        ----------

        state_to_idx : Dict[State, int]
            Mapping from states to indices in boolean matrix
        start_states : Set[State]
            Set of start states
        final_states : Set[State]
            Set of final states
        b_mtx: Dict[Any, dok_matrix]
            Mapping from edge label to boolean adjacency matrix
        """
        self.state_to_idx = state_to_idx
        self.start_states = start_states
        self.final_states = final_states
        self.b_mtx = b_mtx

    def __and__(
        self, other: "BoolMatrixAutomatonPyCuBool"
    ) -> "BoolMatrixAutomatonPyCuBool":
        """Calculates intersection of two automatons represented by bool matrices

        Parameters
        ----------
        other : BoolMatrixAutomatonPyCuBool
            The automaton with which intersection will be calculated

        Returns
        -------
        intersection : BoolMatrixAutomatonPyCuBool
            Intersection of two automatons represented by bool matrix
        """
        inter_labels = self.b_mtx.keys() & other.b_mtx.keys()
        inter_b_mtx = {
            label: self.b_mtx[label].kronecker(other.b_mtx[label])
            for label in inter_labels
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
        return BoolMatrixAutomatonPyCuBool(
            state_to_idx=inter_state_to_idx,
            start_states=inter_start_states,
            final_states=inter_final_states,
            b_mtx=inter_b_mtx,
        )

    def transitive_closure(self) -> Matrix:
        """Calculates transitive closure

        Returns
        -------
        transitive_closure : Matrix
            Transitive closure represented by sparse matrix
        """
        state_count = max(len(self.state_to_idx), 1)
        transitive_closure = Matrix.empty((state_count, state_count))
        for b_mtx in self.b_mtx.values():
            transitive_closure = transitive_closure.ewiseadd(b_mtx)

        prev_nnz, cur_nnz = None, transitive_closure.nvals
        if not cur_nnz:
            return transitive_closure

        while prev_nnz != cur_nnz:
            transitive_closure.mxm(
                transitive_closure, out=transitive_closure, accumulate=True
            )
            prev_nnz, cur_nnz = cur_nnz, transitive_closure.nvals
        return transitive_closure

    @classmethod
    def from_nfa(cls, nfa: EpsilonNFA) -> "BoolMatrixAutomatonPyCuBool":
        """Builds bool matrix from nfa

        Parameters
        ----------
        nfa : EpsilonNFA
            NFA to be converted to bool matrix

        Returns
        -------
        bool_matrix : BoolMatrixAutomatonPyCuBool
            Bool matrix representation of automaton
        """
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

    @staticmethod
    def _b_mtx_from_nfa(
        nfa: EpsilonNFA, state_to_idx: Dict[State, int]
    ) -> Dict[Any, Matrix]:
        """Utility method for creating mapping from labels to adj bool matrix

        Parameters
        ----------
        nfa : EpsilonNFA
            Epsilon NFA from which mapping will be created
        state_to_idx: Dict[State, int]
            Mapping from states to indices in boolean matrix

        Returns
        -------
        b_mtx : Dict[State, int]
            Mapping from labels to adj bool matrix
        """
        b_mtx = dict()
        state_from_to_transitions = nfa.to_dict()
        for label in nfa.symbols:
            mtx = Matrix.empty((len(nfa.states), len(nfa.states)))
            for state_from, transitions in state_from_to_transitions.items():
                states_to = transitions.get(label, set())
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for state_to in states_to:
                    mtx[state_to_idx[state_from], state_to_idx[state_to]] = True
            b_mtx[label] = mtx
        return b_mtx

    def _direct_sum(
        self, other: "BoolMatrixAutomatonPyCuBool"
    ) -> "BoolMatrixAutomatonPyCuBool":
        """Calculates direct sum of automatons represented by bool matrix

        Parameters
        ----------
        other : BoolMatrixAutomatonPyCuBool
            The matrix with which sum will be calculated

        Returns
        -------
        direct_sum : BoolMatrixAutomatonPyCuBool
            Direct sum
        """
        shifted_state_to_idx = {
            state: len(self.state_to_idx) + idx
            for state, idx in other.state_to_idx.items()
        }
        state_to_idx = {**self.state_to_idx, **shifted_state_to_idx}
        start_states = self.start_states | other.start_states
        final_states = self.final_states | other.final_states
        b_mtx = dict()
        for label in self.b_mtx.keys() & other.b_mtx.keys():
            mtx = Matrix.empty((len(state_to_idx), len(state_to_idx)))
            for i, j in self.b_mtx[label]:
                mtx[i, j] = True
            for i, j in other.b_mtx[label]:
                mtx[len(self.state_to_idx) + i, len(self.state_to_idx) + j] = True
            b_mtx[label] = mtx
        return BoolMatrixAutomatonPyCuBool(
            state_to_idx=state_to_idx,
            start_states=start_states,
            final_states=final_states,
            b_mtx=b_mtx,
        )

    def sync_bfs(
        self,
        other: "BoolMatrixAutomatonPyCuBool",
        reachable_per_node: bool,
    ) -> Set[Any]:
        """Executes sync bfs on two automatons represented by bool matrices

        Parameters
        ----------
        other : BoolMatrixAutomatonPyCuBool
            The matrix with which bfs will be executed
        reachable_per_node: bool
            Means calculates reachability for each node separately or not

        Returns
        -------
        result : Set[Any]
            Result depends on reachable_per_node
        if reachable_per_node is false -- set of reachable nodes
        if reachable_per_node is true -- set of tuples (U, V)
        where U is start node and V is final node reachable from U
        """

        if not self.state_to_idx or not other.state_to_idx:
            return set()

        ordered_start_states = list(self.start_states)

        direct_sum = other._direct_sum(self)
        initial_front = self._init_sync_bfs_front(
            other=other,
            reachable_per_node=reachable_per_node,
            ordered_start_states=ordered_start_states,
        )

        front = self._copy_mtx(initial_front)
        visited = self._copy_mtx(front)

        other_states_num = len(other.state_to_idx)

        while True:
            visited_nnz = visited.nvals
            new_front = self._copy_mtx(front)

            for _, mtx in direct_sum.b_mtx.items():
                product: Matrix = front.mxm(mtx)
                new_front_step = Matrix.empty(product.shape)
                for i, j in product:
                    if j >= other_states_num:
                        continue
                    row = product[i : i + 1, other_states_num:]
                    if not row.nvals:
                        continue
                    row_shift = i // other_states_num * other_states_num
                    new_front_step[row_shift + j, j] = True
                    for _, rj in row:
                        new_front_step[row_shift + j, other_states_num + rj] = True
                new_front = new_front.ewiseadd(new_front_step)

            new_front_without_visited = Matrix.empty(new_front.shape)
            for i, j in new_front:
                if not visited[i : i + 1, j : j + 1].to_list():
                    new_front_without_visited[i, j] = True

            visited = visited.ewiseadd(new_front_without_visited)
            front = new_front_without_visited

            if visited_nnz == visited.nvals:
                break

        self_idx_to_state = {idx: state for state, idx in self.state_to_idx.items()}
        other_idx_to_state = {idx: state for state, idx in other.state_to_idx.items()}

        result = set()
        nonzero = set(visited.to_list()).difference(set(initial_front.to_list()))
        for i, j in nonzero:
            if (
                other_idx_to_state[i % other_states_num] not in other.final_states
                or j < other_states_num
            ):
                continue
            self_state = self_idx_to_state[j - other_states_num]
            if self_state not in self.final_states:
                continue
            result.add(
                self_state.value
                if not reachable_per_node
                else (
                    ordered_start_states[i // other_states_num].value,
                    self_state.value,
                )
            )
        return result

    @staticmethod
    def _copy_mtx(matrix: Matrix):
        copy = Matrix.empty(matrix.shape)
        for i, j in matrix:
            copy[i, j] = True
        return copy

    def _init_sync_bfs_front(
        self,
        other: "BoolMatrixAutomatonPyCuBool",
        reachable_per_node: bool,
        ordered_start_states: List[State],
    ) -> Matrix:
        """Initializes front for sync bfs

        Parameters
        ----------
        other : BoolMatrixAutomatonPyCuBool
            The matrix with which bfs will be executed
        reachable_per_node: bool
            Means calculates reachability for each node separately or not
            ordered_start_states: List[State]
            List of start states

        Returns
        -------
        result : csr_matrix
            Initial front for sync bfs
        """

        def front_with_self_start_row(self_start_row: List):
            front = Matrix.empty(
                (
                    len(other.state_to_idx),
                    len(self.state_to_idx) + len(other.state_to_idx),
                )
            )
            for state in other.start_states:
                idx = other.state_to_idx[state]
                front[idx, idx] = True
                for i, item in enumerate(self_start_row):
                    if item:
                        front[idx, len(other.state_to_idx) + i] = item
            return front

        if not reachable_per_node:
            start_indices = set(
                self.state_to_idx[state] for state in ordered_start_states
            )
            return front_with_self_start_row(
                [idx in start_indices for idx in range(len(self.state_to_idx))]
            )

        fronts = [
            front_with_self_start_row(
                [
                    idx == self.state_to_idx[start]
                    for idx in range(len(self.state_to_idx))
                ]
            )
            for start in ordered_start_states
        ]

        mtx = Matrix.empty(
            (
                len(fronts) * len(other.state_to_idx),
                len(other.state_to_idx) + len(self.state_to_idx),
            )
        )
        for front_number, front in enumerate(fronts):
            for i, j in front:
                mtx[len(other.state_to_idx) * front_number + i, j] = True
        return mtx
