import shlex


def parse_value(value):
    """Преобразует строковое значение в нужный тип данных."""

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    try:
        return int(value)
    except ValueError:
        return value


def parse_condition(condition):
    """Разбирает условие вида column = value."""

    parts = shlex.split(condition)

    if len(parts) != 3 or parts[1] != "=":
        raise ValueError("Некорректное условие.")

    column, _, value = parts

    return {column: parse_value(value)}


def parse_set_clause(set_clause):
    """Разбирает несколько присваиваний через запятую."""

    assignments = set_clause.split(",")
    result = {}

    for assignment in assignments:
        condition = parse_condition(assignment)
        result.update(condition)

    return result
