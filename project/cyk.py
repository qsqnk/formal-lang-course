from pyformlang.cfg import CFG

__all__ = [
    "cyk",
]


def cyk(s: str, cfg: CFG) -> bool:
    """Determines whether a word belongs to the language generated
     by the given context free grammar using CYK algorithm

    Parameters
    ----------
    s : str
        Word to be checked

    cfg : CFG
        Context Free Grammar

    Returns
    -------
    result: bool
        Whether a word belongs to the language generated by the grammar
    """
    if not s:
        return cfg.generate_epsilon()

    n = len(s)
    cnf = cfg.to_normal_form()
    dp = [[set() for _ in range(n)] for _ in range(n)]

    prods_body_terminal, prods_body_two_non_terminals = (
        [p for p in cnf.productions if len(p.body) == body_length]
        for body_length in (1, 2)
    )

    for i, c in enumerate(s):
        dp[i][i] = set(p.head for p in prods_body_terminal if p.body[0].value == c)

    for step in range(1, n):
        for i in range(n - step):
            j = i + step
            for k in range(i, j):
                dp[i][j] |= set(
                    p.head
                    for p in prods_body_two_non_terminals
                    if p.body[0] in dp[i][k] and p.body[1] in dp[k + 1][j]
                )

    return cfg.start_symbol in dp[0][n - 1]