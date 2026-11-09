from primitive_db.decorators import (
    confirm_action,
    create_cacher,
    handle_db_errors,
    log_time,
)

cache_result = create_cacher()

# Поддерживаемые типы данных
SUPPORTED_TYPES = {"int", "str", "bool"}

@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создаёт таблицу и добавляет её структуру в метаданные."""

    # Проверяем, существует ли таблица
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    # Проверяем корректность типов столбцов
    for column_name, column_type in columns:
        if column_type not in SUPPORTED_TYPES:
            print(f"Некорректное значение: {column_type}. Попробуйте снова.")
            return metadata

    # Добавляем автоматически создаваемый столбец ID
    table_columns = {"ID": "int"}

    # Добавляем пользовательские столбцы
    for column_name, column_type in columns:
        if column_name == "ID":
            print("Некорректное значение: ID. Попробуйте снова.")
            return metadata

        table_columns[column_name] = column_type

    # Сохраняем структуру новой таблицы
    metadata[table_name] = table_columns

    print(
        f'Таблица "{table_name}" успешно создана '
        f"со столбцами: "
        + ", ".join(f"{name}:{type_}" for name, type_ in table_columns.items())
    )

    return metadata

@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""

    # Проверяем существование таблицы
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    # Удаляем таблицу
    metadata = metadata.copy()
    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def list_tables(metadata):
    """Выводит список всех таблиц базы данных."""

    # Проверяем, есть ли таблицы в базе данных
    if not metadata:
        print("В базе данных пока нет таблиц.")
        return

    # Выводим названия всех таблиц
    for table_name in metadata:
        print(f"- {table_name}")

@log_time
@handle_db_errors
def insert(metadata, table_name, values, table_data):
    """Добавляет новую запись в таблицу."""

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = metadata[table_name]

    # Исключаем автоматически создаваемый ID
    user_columns = {name: type_ for name, type_ in columns.items() if name != "ID"}

    # Проверяем количество значений
    if len(values) != len(user_columns):
        print("Ошибка: Количество значений не соответствует количеству столбцов.")
        return table_data

    # Проверяем типы значений
    for value, column_type in zip(values, user_columns.values()):
        if column_type == "int" and type(value) is not int:
            print("Ошибка: Ожидается значение типа int.")
            return table_data

        if column_type == "str" and not isinstance(value, str):
            print("Ошибка: Ожидается значение типа str.")
            return table_data

        if column_type == "bool" and not isinstance(value, bool):
            print("Ошибка: Ожидается значение типа bool.")
            return table_data

    # Генерируем новый ID
    new_id = max((row["ID"] for row in table_data), default=0) + 1

    # Создаём запись
    new_record = {"ID": new_id}
    new_record.update(zip(user_columns.keys(), values))

    table_data.append(new_record)

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')

    return table_data

@log_time
@handle_db_errors
def select(table_data, where_clause=None):
    cache_key = (
        tuple(tuple(sorted(row.items())) for row in table_data),
        tuple(sorted(where_clause.items())) if where_clause else None,
    )

    def get_result():
        if where_clause is None:
            return table_data

        return [
            row
            for row in table_data
            if all(row.get(key) == value for key, value in where_clause.items())
        ]

    return cache_result(cache_key, get_result)

@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет записи по заданному условию."""

    for row in table_data:
        if all(row.get(key) == value for key, value in where_clause.items()):
            row.update(set_clause)

    return table_data

@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    """Удаляет записи по заданному условию."""

    remaining_data = [
        row
        for row in table_data
        if not all(row.get(key) == value for key, value in where_clause.items())
    ]

    return remaining_data

@handle_db_errors
def info(metadata, table_name, table_data):
    """Выводит информацию о таблице."""

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    print(f'\nИнформация о таблице "{table_name}":')

    print("Столбцы:")
    for column_name, column_type in metadata[table_name].items():
        print(f"- {column_name}: {column_type}")

    print(f"Количество записей: {len(table_data)}")
