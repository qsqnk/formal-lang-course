grammar GQL;

program : (EOL? WS? stmt SEMI EOL?)+ EOF;

stmt :
    var EQUALS expr
    | PRINT LPAREN expr RPAREN
;

var : ID;
bool: 'true' | 'false' ;
val : bool | INT | STR;

expr :
    val
    | var
    | bool_expr
    | graph
    | filter_
    | map_
    | vertex
    | vertices
    | vertices_pair
    | edge
    | edges
    | label
    | labels
;

filter_ : FILTER LPAREN lambda_ COMMA expr RPAREN;
map_ : MAP LPAREN lambda_ COMMA expr RPAREN;

graph :
    var
    | SYMBOL LPAREN val RPAREN
    | LOAD LPAREN STR RPAREN
    | SET_START LPAREN vertices COMMA graph RPAREN
    | SET_FINAL LPAREN vertices COMMA graph RPAREN
    | ADD_START LPAREN vertices COMMA graph RPAREN
    | ADD_FINAL LPAREN vertices COMMA graph RPAREN
    | INTERSECT LPAREN graph COMMA graph RPAREN
    | CONCAT LPAREN graph COMMA graph RPAREN
    | UNION LPAREN graph COMMA graph RPAREN
    | STAR LPAREN graph RPAREN
    | CFG LPAREN STR RPAREN
;

vertex : var | INT;

vertices :
    var
    | LCURLY (vertex COMMA)* (vertex)? RCURLY
    | RANGE LPAREN INT COMMA INT RPAREN
    | GET_START LPAREN graph RPAREN
    | GET_FINAL LPAREN graph RPAREN
    | GET_VERTICES LPAREN graph RPAREN
    | filter_
    | map_
;
vertices_pair :
    var
    | LCURLY (LPAREN vertex COMMA vertex RPAREN COMMA)* (LPAREN vertex COMMA vertex RPAREN)? RCURLY
    | GET_REACHABLE LPAREN graph RPAREN
;
edge :
    var
    | LPAREN vertex COMMA label COMMA vertex RPAREN
    ;

edges :
    var
    | LCURLY (edge COMMA)* (edge)? RCURLY
    | GET_EDGES LPAREN graph RPAREN
    | filter_
    | map_
   ;

label : val | var;

labels :
    var
    | LCURLY (label COMMA)* (label)? RCURLY
    | GET_LABELS LPAREN graph RPAREN
    | filter_
    | map_
    ;

bool_expr :
    bool
    | var
    | bool_expr OR bool_expr
    | bool_expr AND bool_expr
    | NOT bool_expr
    | HAS_LABEL LPAREN edge COMMA label
    | IS_START LPAREN vertex LPAREN
    | IS_FINAL LPAREN vertex LPAREN
    | vertex IN vertices
    | label IN labels
;

lambda_ : LPAREN ((var COMMA)* (var)?) RARROW expr RPAREN;

SEMI : ';' ;

LPAREN : '(' ;
RPAREN : ')' ;
LCURLY : '{' ;
RCURLY : '}' ;

EQUALS : '=' ;
COMMA : ',' ;
RARROW : '->' ;
UNDER : '_' ;

PRINT : 'print' ;

SET_START : 'set_start' ;
SET_FINAL : 'set_final' ;
ADD_START : 'add_start' ;
ADD_FINAL : 'add_final' ;
GET_START : 'get_start' ;
GET_FINAL : 'get_final' ;
GET_VERTICES : 'get_vertices' ;
GET_EDGES : 'get_edges' ;
GET_LABELS : 'get_labels' ;
GET_REACHABLE : 'get_reachable' ;
MAP : 'map' ;
FILTER : 'filter' ;
LOAD : 'load' ;
SYMBOL : 'symbol' ;
INTERSECT : 'intersect' ;
UNION : 'union' ;
CONCAT : 'concat' ;
STAR : 'star' ;
CFG : 'cfg' ;

OR : 'or' ;
AND : 'and' ;
IN : 'in' ;
NOT : 'not' ;
HAS_LABEL : 'has_label' ;
IS_START : 'is_start' ;
IS_FINAL : 'is_final' ;

RANGE : 'range';

ID : [_a-zA-Z][_a-zA-Z0-9]* ;
INT : '0' | '-'? [1-9][0-9]* ;
STR : '"' .*? '"' ;

WS : [ \t\r]+ -> skip;
EOL : [\n]+;
