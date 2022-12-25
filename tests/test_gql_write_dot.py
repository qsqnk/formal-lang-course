import pytest

from project.gql.parsing import *


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "x = 5;",
            """
strict digraph parse_tree {
0 [label=program];
1 [label=stmt];
0 -> 1;
2 [label=var];
1 -> 2;
3 [label="'x'", shape=box];
2 -> 3;
4 [label="'='", shape=box];
1 -> 4;
5 [label=expr];
1 -> 5;
6 [label=val];
5 -> 6;
7 [label="'5'", shape=box];
6 -> 7;
8 [label="';'", shape=box];
0 -> 8;
9 [label="'<EOF>'", shape=box];
0 -> 9;
}
            """,
        ),
        (
            'print(intersect(load("g1"), load("g2")));',
            """
strict digraph parse_tree {
0 [label=program];
1 [label=stmt];
0 -> 1;
2 [label="'print'", shape=box];
1 -> 2;
3 [label="'('", shape=box];
1 -> 3;
4 [label=expr];
1 -> 4;
5 [label=graph];
4 -> 5;
6 [label="'intersect'", shape=box];
5 -> 6;
7 [label="'('", shape=box];
5 -> 7;
8 [label=graph];
5 -> 8;
9 [label="'load'", shape=box];
8 -> 9;
10 [label="'('", shape=box];
8 -> 10;
11 [label="\'\\"g1\\"\'", shape=box];
8 -> 11;
12 [label="')'", shape=box];
8 -> 12;
13 [label="','", shape=box];
5 -> 13;
14 [label=graph];
5 -> 14;
15 [label="'load'", shape=box];
14 -> 15;
16 [label="'('", shape=box];
14 -> 16;
17 [label="\'\\"g2\\"\'", shape=box];
14 -> 17;
18 [label="')'", shape=box];
14 -> 18;
19 [label="')'", shape=box];
5 -> 19;
20 [label="')'", shape=box];
1 -> 20;
21 [label="';'", shape=box];
0 -> 21;
22 [label="'<EOF>'", shape=box];
0 -> 22;
}
            """,
        ),
    ],
)
def test_write_dot(tmpdir, text, expected):
    file = tmpdir.mkdir("test_dir").join("some_cfg_file")
    save_parse_tree_as_dot(text, file)
    print(file.read())
    assert file.read().strip() == expected.strip()
