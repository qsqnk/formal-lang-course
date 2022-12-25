from typing import Callable, Any, Union, IO

import antlr4
import pydot

from project.gql.GQLLexer import GQLLexer
from project.gql.GQLParser import GQLParser
from project.gql.GQLListener import GQLListener

__all__ = [
    "check",
    "save_parse_tree_as_dot",
]


def _get_parser(input: str) -> GQLParser:
    """Returns GQL parser by input

    Parameters
    ----------
    input : str
        Input

    Returns
    -------
    parser : GQLParser
        Parser
    """
    chars = antlr4.InputStream(input)
    lexer = GQLLexer(chars)
    tokens = antlr4.CommonTokenStream(lexer)
    return GQLParser(tokens)


def check(
    input: str,
    parse_func: Callable[[GQLParser], Any] = lambda p: p.program(),
) -> bool:
    """Checks that the input is recognized by passed GQL parser

    Parameters
    ----------
    input : str
        Input

    parse_func: Callable[[GQLParser], Any]
        Function that executes one of the parser rules

    Returns
    -------
    result : bool
        Has input been successfully recognized
    """
    parser = _get_parser(input)
    parser.removeErrorListeners()
    parse_func(parser)
    return parser.getNumberOfSyntaxErrors() == 0


def save_parse_tree_as_dot(input: str, file: Union[str, IO]) -> None:
    """Saves parse tree as dot

    Parameters
    ----------
    input : str
        Input

    file: Union[str, IO]
        The name of file or file itself
    """
    parser = _get_parser(input)
    if parser.getNumberOfSyntaxErrors() > 0:
        raise ValueError("Bad gql syntax")
    builder = _DotTreeBuilder()
    walker = antlr4.ParseTreeWalker()
    walker.walk(builder, parser.program())
    builder.dot.write(str(file))


class _DotTreeBuilder(GQLListener):
    def __init__(self):
        self.dot = pydot.Dot("parse_tree", strict=True)
        self._curr_id = 0
        self._id_stack = []

    # overriden method
    def enterEveryRule(self, ctx: antlr4.ParserRuleContext):
        self.dot.add_node(
            pydot.Node(self._curr_id, label=GQLParser.ruleNames[ctx.getRuleIndex()])
        )
        if len(self._id_stack) > 0:
            self.dot.add_edge(pydot.Edge(self._id_stack[-1], self._curr_id))
        self._id_stack.append(self._curr_id)
        self._curr_id += 1

    # overriden method
    def exitEveryRule(self, ctx: antlr4.ParserRuleContext):
        self._id_stack.pop()

    # overriden method
    def visitTerminal(self, node: antlr4.TerminalNode):
        self.dot.add_node(pydot.Node(self._curr_id, label=f"'{node}'", shape="box"))
        self.dot.add_edge(pydot.Edge(self._id_stack[-1], self._curr_id))
        self._curr_id += 1
