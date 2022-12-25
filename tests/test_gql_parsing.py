import pytest

from project.gql.parsing import *


@pytest.mark.parametrize(
    "text, accept",
    [
        ("_abc", True),
        ("Abc", True),
        ("1a", False),
        ("!", False),
    ],
)
def test_var(text, accept):
    assert check(text, lambda p: p.var()) == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("1", True),
        ("-1", True),
        ('"str"', True),
        ("true", True),
    ],
)
def test_val(text, accept):
    assert check(text, lambda p: p.val()) == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ('load("wine")', True),
        ("star(x)", True),
        ("intersect(g1, g2)", True),
        ("map((x -> true), vertices)", True),
        ("map(x -> true, vertices)", False),
        ("load $ wine", False),
    ],
)
def test_expr(text, accept):
    assert check(text, lambda p: p.expr()) == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("x = 5", True),
        ("print(1)", True),
        ("y = intersect(star(g), intersect(star(g1), star(g2)))", True),
        ("x", False),
        ('load("graph")', False),
    ],
)
def test_statement(text, accept):
    assert check(text, lambda p: p.stmt()) == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        (
            """
            raw_graph = load("some_graph");
            vertices = get_vertices(raw);

            raw_graph_1 = set_start(vertices, raw_graph);
            raw_graph_2 = set_final(filter((v -> v in vertices), range(1, 10)), raw_graph_1);
            ready_graph = raw_graph_2;
            query = star(concat(symbol("abc"), star(symbol("def"))));
            print(intersect(ready_graph, query));
            """,
            True,
        ),
        (
            """
            print(intersect(ready_graph, query));
            """,
            True,
        ),
        (
            """
            print(intersect(ready_graph, query))
            """,
            False,
        ),
    ],
)
def test_program(text, accept):
    assert check(text, lambda p: p.program()) == accept
