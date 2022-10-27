from project import RSM

__all__ = [
    "minimize_rsm",
]


def minimize_rsm(rsm: RSM) -> RSM:
    """Minimizes RSM by minimising internal automatons

    Parameters
    ----------
    rsm : RSM
        Recursive state machine

    Returns
    -------
    minimised_rsm : RSM
        Minimized recursive state machine
    """
    return RSM(
        start_symbol=rsm.start_symbol,
        boxes={v: a.minimize() for v, a in rsm.boxes},
    )
