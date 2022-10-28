import pytest

from project.ecfg import *
from project.cfg_utils import *
from project.rsm_utils import *
from tests.utils import check_automatons_are_equivalent


@pytest.mark.parametrize(
    "corresponding_ecfg_as_text",
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
def test_minimize_rsm(corresponding_ecfg_as_text):
    rsm = ecfg_to_rsm(ECFG.from_text(corresponding_ecfg_as_text))
    minimized = minimize_rsm(rsm)
    assert all(
        check_automatons_are_equivalent(
            automaton,
            automaton.minimize(),
        )
        for automaton in minimized.boxes.values()
    )
