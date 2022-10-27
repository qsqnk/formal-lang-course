from collections import defaultdict
from functools import reduce
from typing import Union, List

from pyformlang.cfg import CFG, Variable
from pyformlang.cfg.cfg_object import CFGObject
from pyformlang.regular_expression import Regex
from typing.io import IO

__all__ = [
    "cfg_to_wcnf",
    "cfg_from_file",
    "cfg_to_ecfg",
    "ecfg_from_file",
    "ecfg_to_rsm",
]

from project.rsm import RSM
from project.ecfg import ECFG


def cfg_to_wcnf(cfg: CFG) -> CFG:
    """Converts CFG to Weak Chomsky Normal Form

    Parameters
    ----------
    cfg : CFG
        Context free grammar

    Returns
    -------
    wcnf: CFG
        Converted cfg
    """
    cleared = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    productions = cleared._decompose_productions(
        cleared._get_productions_with_only_single_terminals()
    )
    return CFG(start_symbol=cleared.start_symbol, productions=set(productions))


def cfg_from_file(
    file: Union[str, IO], start_symbol: Union[str, Variable] = Variable("S")
) -> CFG:
    """Loads CFG from file

    Parameters
    ----------
    file : Union[str, IO]
        Filename or file itself
    start_symbol : Union[str, Variable]
        The start symbol for the CFG to be loaded

    Returns
    -------
    cfg: CFG
        Loaded CFG
    """
    with open(file) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)


def cfg_to_ecfg(cfg: CFG) -> ECFG:
    """Converts CFG to ECFG

    Parameters
    ----------
    cfg : CFG
        Context free grammar to be converted

    Returns
    -------
    ecfg: ECFG
        Extended context free grammar
    """
    productions = defaultdict(list)
    for p in cfg.productions:
        productions[p.head].append(p.body)
    return ECFG(
        start_symbol=cfg.start_symbol,
        variables=cfg.variables,
        productions={
            h: reduce(Regex.union, map(concat_body, bodies))
            for h, bodies in productions
        },
    )


def ecfg_from_file(
    file: Union[str, IO], start_symbol: Union[str, Variable] = Variable("S")
) -> ECFG:
    """Loads ECFG from file

    Parameters
    ----------
    file : Union[str, IO]
        Filename or file itself
    start_symbol : Union[str, Variable]
        The start symbol for the ECFG to be loaded

    Returns
    -------
    ecfg: ECFG
        Loaded ECFG
    """
    with open(file) as f:
        return ECFG.from_text(f.read(), start_symbol=start_symbol)


def ecfg_to_rsm(ecfg: ECFG) -> RSM:
    """Converts ECFG to RSM

    Parameters
    ----------
    ecfg : ECFG
        Extended context free grammar to be converted

    Returns
    -------
    rsm: RSM
        Recursive state machine
    """
    return RSM(
        start_symbol=ecfg.start_symbol,
        boxes={h: r.to_epsilon_nfa().to_deterministic() for h, r in ecfg.productions},
    )


def concat_body(body: List[CFGObject]) -> Regex:
    """Utility function for converting body of CFG production to regex

    Parameters
    ----------
    body : List[CFGObject]
        Body of CFG production

    Returns
    -------
    regex: Regex
        Regular expression
    """
    return reduce(Regex.concatenate, [Regex(o.value) for o in body], initial=Regex(""))
