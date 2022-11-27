import pytest
from pyformlang.cfg import CFG

from project.ecfg import *
from project.matrix_utils import *


@pytest.mark.parametrize(
    "cfg_as_text, expected_start_idx, expected_final_idx, expected_b_mtx",
    [
        (
            """
            S ->
            """,
            {0},
            {0},
            {},
        ),
        (
            """
            S -> a
            """,
            {0},
            {1},
            {"a": [[False, True], [False, False]]},
        ),
        (
            """
            S ->
            S -> a S b
            """,
            {0},
            {0, 1},
            {
                "a": [
                    [False, False, False, True],
                    [False, False, False, False],
                    [False, False, False, False],
                    [False, False, False, False],
                ],
                "S": [
                    [False, False, False, False],
                    [False, False, False, False],
                    [False, False, False, False],
                    [False, False, True, False],
                ],
                "b": [
                    [False, False, False, False],
                    [False, False, False, False],
                    [False, True, False, False],
                    [False, False, False, False],
                ],
            },
        ),
    ],
)
def test_bool_matrix_from_rsm(
    cfg_as_text, expected_start_idx, expected_final_idx, expected_b_mtx
):
    cfg = CFG.from_text(cfg_as_text)
    rsm = ECFG.from_cfg(cfg).to_rsm()
    bool_mtx = BoolMatrixAutomaton.from_rsm(rsm)
    assert all(
        (
            {bool_mtx.state_to_idx[s] for s in bool_mtx.start_states}
            == expected_start_idx,
            {bool_mtx.state_to_idx[s] for s in bool_mtx.final_states}
            == expected_final_idx,
            {k: v.toarray().tolist() for k, v in bool_mtx.b_mtx.items()}
            == expected_b_mtx,
        )
    )
