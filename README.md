[![Check code style](https://github.com/JetBrains-Research/formal-lang-course/actions/workflows/code_style.yml/badge.svg)](https://github.com/JetBrains-Research/formal-lang-course/actions/workflows/code_style.yml)
[![Code style](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)
---
# Formal Language Course

Курс по формальным языкам: шаблон структуры репозитория для выполнения домашних работ,
а также материалы курса и другая сопутствующая информация.

Актуальное:
- [Таблица с текущими результатами](https://docs.google.com/spreadsheets/d/1IXeAhVb_cRRQf0UwHjw2AeBqNwpcY-XcnVs3-t9HBYc/edit#gid=0)
- [Список задач](https://github.com/JetBrains-Research/formal-lang-course/tree/main/tasks)
- [Стиль кода как референс](https://www.python.org/dev/peps/pep-0008/)
- [Материалы по курсу](https://github.com/JetBrains-Research/formal-lang-course/blob/main/docs/lecture_notes/Formal_language_course.pdf)
- [О достижимости с ограничениями в терминах формальных языков](https://github.com/JetBrains-Research/FormalLanguageConstrainedReachability-LectureNotes)

Технологии:
- Python 3.8+
- Pytest для unit тестирования
- GitHub Actions для CI
- Google Colab для постановки и оформления экспериментов
- Сторонние пакеты из `requirements.txt` файла
- Английский язык для документации или самодокументирующийся код

## Работа с проектом

- Для выполнения домашних практических работ необходимо сделать **приватный** `fork` этого репозитория к себе в `GitHub`.
- Рекомендуется установить [`pre-commit`](https://pre-commit.com/#install) для поддержания проекта в адекватном состоянии.
  - Установить `pre-commit` можно выполнив следующую команду в корне вашего проекта:
    ```shell
    pre-commit install
    ```
  - Отформатировать код в соответствии с принятым стилем можно выполнив следующую команду в корне вашего проекта:
    ```shell
    pre-commit run --all-files
    ```
- Ссылка на свой `fork` репозитория размещается в [таблице](https://docs.google.com/spreadsheets/d/18DhYG5CuOrN4A5b5N7-mEDfDkc-7BuXF3Qsu6HD-lks/edit?usp=sharing) курса с результатами.
- В свой репозиторий необходимо добавить проверяющих с `admin` правами на чтение, редактирование и проверку `pull-request`'ов.

## Домашние практические работы

### Дедлайны

- **мягкий**: воскресенье 23:59
- **жёсткий**: среда 23:59

### Выполнение домашнего задания

- Каждое домашнее задание выполняется в отдельной ветке. Ветка должна иметь осмысленное консистентное название.
- При выполнении домашнего задания в новой ветке необходимо открыть соответствующий `pull-request` в `main` вашего `fork`.
- `Pull-request` снабдить понятным названием и описанием с соответствующими пунктами прогресса.
- Проверка заданий осуществляется посредством `review` вашего `pull-request`.
- Как только вы считаете, что задание выполнено, вы можете запросить `review` у проверяющего.
  - Если `review` запрошено **до мягкого дедлайна**, то вам гарантированна дополнительная проверка (до жёсткого дедлайна), позволяющая исправить замечания до наступления жёсткого дедлайна.
  - Если `review` запрошено **после мягкого дедлайна**, но **до жесткого дедлайна**, задание будет проверено, но нет гарантий, что вы успеете его исправить.
- Когда проверка будет пройдена, и задание **зачтено**, его необходимо `merge` в `main` вашего `fork`.
- Результаты выполненных заданий будут повторно использоваться в последующих домашних работах.

### Опциональные домашние задания
Часть задач, связанных с работой с GPGPU, будет помечена как опциональная. Это означает что и без их выполнения (при идеальном выполнении остальных задач) можно набрать полный балл за курс.

### Получение оценки за домашнюю работу

- Если ваша работа **зачтена** _до_ **жёсткого дедлайна**, то выполучаете **полный балл за домашнюю работу**.
- Если ваша работа **зачтена** _после_ **жёсткого дедлайна**, то вы получаете **половину полного балла за домашнюю работу**.

## Код

- Исходный код практических задач по программированию размещайте в папке `project`.
- Файлам и модулям даем осмысленные имена, в соответствии с официально принятым стилем.
- Структурируем код, используем как классы, так и отдельно оформленные функции. Чем понятнее код, тем быстрее его проверять и тем больше у вас будет шансов получить полный балл.

## Тесты

- Тесты для домашних заданий размещайте в папке `tests`.
- Формат именования файлов с тестами `test_[какой модуль\класс\функцию тестирует].py`.
- Для работы с тестами рекомендутеся использовать [`pytest`](https://docs.pytest.org/en/6.2.x/).
- Для запуска тестов необходимо из корня проекта выполнить следующую команду:
  ```shell
  python ./scripts/run_tests.py
  ```

## Эксперименты

- Для выполнения экспериментов потребуется не только код, но окружение и некоторая его настройка.
- Эксперименты должны быть воспроизводимыми (например, проверяющими).
- Эксперимент (настройка, замеры, результаты, анализ результатов) оформляется как Python-ноутбук, который публикуется на GitHub.
  - В качестве окружения для экспериментов с GPGPU (опциональные задачи) можно использовать [`Google Colab`](https://research.google.com/colaboratory/) ноутбуки. Для его создания требуется только учетная запись `Google`.
  - В `Google Colab` ноутбуке выполняется вся настройка, пишется код для экспериментов, подготовки отчетов и графиков.

## Структура репозитория

```text
.
├── .github - файлы для настройки CI и проверок
├── docs - текстовые документы и материалы по курсу
├── project - исходный код домашних работ
├── scripts - вспомогательные скрипты для автоматизации разработки
├── tasks - файлы с описанием домашних заданий
├── tests - директория для unit-тестов домашних работ
├── README.md - основная информация о проекте
└── requirements.txt - зависимости для настройки репозитория
```

## Контакты

- Семен Григорьев [@gsvgit](https://github.com/gsvgit)
- Егор Орачев [@EgorOrachyov](https://github.com/EgorOrachyov)
- Вадим Абзалов [@vdshk](https://github.com/vdshk)
- Рустам Азимов [@rustam-azimov](https://github.com/rustam-azimov)
- Екатерина Шеметова [@katyacyfra](https://github.com/katyacyfra)

## Язык запросов к графам

### Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda =
    Lambda of List<var> * expr
```

### Описание конкретного синтаксиса языка

```
PROGRAM ->
    STMT ; PROGRAM
    | eps

STMT ->
    VAR = EXPR
    | PRINT(EXPR)

LOWERCASE -> [a-z]
UPPERCASE -> [A-Z]

DIGIT -> [0-9]
INT ->
    [1-9] DIGIT*
    | 0
BOOL ->
    true
    | false

STR -> (_ | . | LOWERCASE | UPPERCASE) (_ | . | LOWERCASE | UPPERCASE | DIGIT)*
PATH -> " (/ | _ | . | LOWERCASE | UPPERCASE | DIGIT)+ "

VAR -> STR
VAL ->
    INT
    | " STR "
    | BOOL

EXPR ->
    VAR
    | VAL
    | GRAPH
    | VERTEX
    | VERTICES
    | VERTICES_PAIR
    | EDGE
    | EDGES
    | LABEL
    | LABELS
    | FILTER
    | MAP

FILTER = filter(LAMBDA, EXPR)
MAP = map(LAMBDA, EXPR)

GRAPH ->
    VAR
    | symbol(VAL)
    | load(PATH)
    | set_start(VERTICES, GRAPH)
    | set_final(VERTICES, GRAPH)
    | add_start(VERTICES, GRAPH)
    | add_final(VERTICES, GRAPH)
    | intersect(GRAPH, GRAPH)
    | concat(GRAPH, GRAPH)
    | union(GRAPH, GRAPH)
    | star(GRAPH, GRAPH)

VERTEX -> VAR | INT

VERTICES ->
    VAR
    | SET<VERTEX>
    | range ( INT , INT )
    | get_start(GRAPH)
    | get_final(GRAPH)
    | get_vertices(GRAPH)
    | FILTER
    | MAP

VERTICES_PAIR ->
    VAR
    | SET<(INT, INT)>
    | get_reachable(GRAPH)

EDGE ->
    VAR
    | (INT, LABEL, INT)

EDGES ->
    VAR
    | SET<EDGE>
    | get_edges(GRAPH)
    | FILTER
    | MAP

LABEL ->
    VAR
    | VAL

LABELS ->
    VAR
    | SET<LABEL>
    | get_labels(GRAPH)
    | FILTER
    | MAP

BOOL_EXPR ->
    VAR
    | BOOL_EXPR or BOOL_EXPR
    | BOOL_EXPR and BOOL_EXPR
    | not BOOL_EXPR
    | BOOL
    | has_label(EDGE, LABEL)
    | is_start(VERTEX)
    | is_final(VERTEX)
    | VERTEX in VERTICES
    | LABEL in LABELS

LAMBDA -> (LIST<VAR> -> [BOOL_EXPR | EXPR])

LIST<T> -> list(T [, T]*) | list()
SET<T> -> set(T [, T]*) | set()
```

### Пример программы

* Получаем граф с именем `some_graph`
* Получаем его вершины
* Устанавливаем стартовыми вершинами все вершины графа
* Устанавливаем финальными вершинами вершины из полуинтервала `[1, 10)`, которые принадлежат множеству вершин графа
* Формируем регулярный запрос
* Печатаем результат запроса к графу

```
raw_graph = load("some_graph");
vertices = get_vertices(raw);

raw_graph_1 = set_start(vertices, raw_graph);
raw_graph_2 = set_final(filter((v -> v in vertices), range(1, 10)), raw_graph_1);

ready_graph = raw_graph_2;
query = star(concat(symbol("abc"), star(symbol("def"))));

print(intersect(ready_graph, query));
```
