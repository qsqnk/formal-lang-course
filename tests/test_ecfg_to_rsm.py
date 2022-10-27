import pytest

from project import ECFG, ecfg_to_rsm, regex_to_min_dfa
from tests.utils import check_automatons_are_equivalent


@pytest.mark.parametrize(
    "ecfg_as_text",
    [
        """
        """,
        """
        S -> a | b
        """,
        """
        S -> (a | b)* | c
        """,
        """
        S -> (d*) | (a b c)
        """,
    ],
)
def test_ecfg_to_rsm(ecfg_as_text):
    ecfg = ECFG.from_text(ecfg_as_text)
    rsm = ecfg_to_rsm(ecfg)
    assert len(ecfg.productions) == len(rsm.boxes)
    assert all(
        check_automatons_are_equivalent(
            regex_to_min_dfa(ecfg.productions[v]),
            rsm.boxes[v].minimize(),
        )
        for v in ecfg.productions
    )
