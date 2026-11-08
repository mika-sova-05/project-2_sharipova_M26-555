import csv
import re
import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.parser import parse_condition, parse_set_clause, parse_value
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

# Имя файла для хранения метаданных базы данных
DB_FILE = "db_meta.json"


def print_help():
    """Выводит справочную информацию о командах базы данных."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> "
        "<столбец1:тип> <столбец2:тип> .. - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> info <имя_таблицы> - информация о таблице")
    print(
        "<command> insert into <имя_таблицы> values "
        "(значение1, значение2, ...) - добавить запись"
    )
    print(
        "<command> select from <имя_таблицы> "
        "[where столбец = значение] - вывести записи"
    )
    print(
        "<command> update <имя_таблицы> set столбец = значение "
        "where столбец = значение - обновить запись"
    )
    print(
        "<command> delete from <имя_таблицы> where столбец = значение - удалить запись"
    )
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def parse_insert_values(values_string):
    """Разбирает значения для команды insert."""

    values = next(csv.reader([values_string], skipinitialspace=True))

    return [parse_value(value) for value in values]


def run():
    """Запускает интерактивную работу с базой данных."""

    print("***База данных***")
    print_help()

    while True:
        # Загружаем актуальные метаданные
        metadata = load_metadata(DB_FILE)

        # Получаем команду пользователя
        user_input = prompt.string("Введите команду: ")

        try:
            # Разделяем введённую строку на команду и аргументы
            args = shlex.split(user_input)
        except ValueError:
            print("Некорректный формат команды. Попробуйте снова.")
            continue

        # Проверяем, что пользователь что-то ввёл
        if not args:
            print("Команда не может быть пустой.")
            continue

        command = args[0]

        if command == "exit":
            print("До свидания!")
            break

        elif command == "help":
            print_help()

        elif command == "list_tables":
            if len(args) != 1:
                print(f"Некорректное значение: {' '.join(args[1:])}. Попробуйте снова.")
                continue

            list_tables(metadata)

        elif command == "info":
            if len(args) != 2:
                print("Укажите название одной таблицы.")
                continue

            table_name = args[1]
            table_data = load_table_data(table_name)

            info(metadata, table_name, table_data)

        elif command == "insert":
            match = re.fullmatch(
                r"insert\s+into\s+(\w+)\s+values\s*\((.*)\)\s*",
                user_input,
            )

            if not match:
                print("Некорректный формат команды insert.")
                continue

            table_name = match.group(1)
            values = parse_insert_values(match.group(2))

            table_data = load_table_data(table_name)
            old_length = len(table_data)

            table_data = insert(metadata, table_name, values, table_data)

            if len(table_data) > old_length:
                save_table_data(table_name, table_data)

        elif command == "select":
            match = re.fullmatch(
                r"select\s+from\s+(\w+)(?:\s+where\s+(.+))?\s*",
                user_input,
            )

            if not match:
                print("Некорректный формат команды select.")
                continue

            table_name = match.group(1)

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            where_clause = parse_condition(match.group(2)) if match.group(2) else None

            table_data = load_table_data(table_name)
            selected_data = select(table_data, where_clause)

            table = PrettyTable()
            table.field_names = list(metadata[table_name].keys())

            for row in selected_data:
                table.add_row([row[column] for column in table.field_names])

            print(table)

        elif command == "update":
            match = re.fullmatch(
                r"update\s+(\w+)\s+set\s+(.+)\s+where\s+(.+)",
                user_input,
            )

            if not match:
                print("Некорректный формат команды update.")
                continue

            table_name = match.group(1)

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            set_clause = parse_set_clause(match.group(2))
            where_clause = parse_condition(match.group(3))

            table_data = load_table_data(table_name)

            old_data = [row.copy() for row in table_data]

            table_data = update(table_data, set_clause, where_clause)

            if table_data != old_data:
                save_table_data(table_name, table_data)
                print(f'Таблица "{table_name}" успешно обновлена.')
            else:
                print("Записи для обновления не найдены.")

        elif command == "delete":
            match = re.fullmatch(
                r"delete\s+from\s+(\w+)\s+where\s+(.+)",
                user_input,
            )

            if not match:
                print("Некорректный формат команды delete.")
                continue

            table_name = match.group(1)

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            where_clause = parse_condition(match.group(2))

            table_data = load_table_data(table_name)
            old_data = [row.copy() for row in table_data]

            table_data = delete(table_data, where_clause)

            if table_data != old_data:
                save_table_data(table_name, table_data)
                print(f'Записи из таблицы "{table_name}" успешно удалены.')
            else:
                print("Записи для удаления не найдены.")

        elif command == "create_table":
            if len(args) < 3:
                print(
                    "Некорректное значение: недостаточно аргументов. Попробуйте снова."
                )
                continue

            table_name = args[1]
            columns = []

            # Разбираем описания столбцов
            for column in args[2:]:
                if ":" not in column:
                    print(f"Некорректное значение: {column}. Попробуйте снова.")
                    break

                column_name, column_type = column.split(":", 1)

                if not column_name or not column_type:
                    print(f"Некорректное значение: {column}. Попробуйте снова.")
                    break

                columns.append((column_name, column_type))
            else:
                old_metadata = metadata.copy()
                metadata = create_table(metadata, table_name, columns)

                if metadata != old_metadata:
                    save_metadata(DB_FILE, metadata)

        elif command == "drop_table":
            if len(args) != 2:
                print(
                    "Некорректное количество аргументов для drop_table. "
                    "Попробуйте снова."
                )
                continue

            old_metadata = metadata.copy()
            metadata = drop_table(metadata, args[1])

            if metadata != old_metadata:
                save_metadata(DB_FILE, metadata)

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
