import json
from pathlib import Path

# Директория для хранения данных таблиц
DATA_DIR = Path("data")


def load_metadata(filepath):
    """Загружает метаданные базы данных из JSON-файла."""
    try:
        # Открываем JSON-файл для чтения в кодировке UTF-8
        with open(filepath, "r", encoding="utf-8") as file:
            # Преобразуем содержимое JSON-файла в Python-словарь
            return json.load(file)

    except FileNotFoundError:
        # Если файл не найден, возвращаем пустой словарь
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные базы данных в JSON-файл."""

    # Открываем файл для записи (если файла нет, он будет создан)
    with open(filepath, "w", encoding="utf-8") as file:
        # Записываем Python-словарь в JSON-файл
        # ensure_ascii=False сохраняет русские символы
        # indent=4 задаёт красивое форматирование с отступами
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_table_data(table_name):
    """Загружает данные таблицы из JSON-файла."""

    filepath = DATA_DIR / f"{table_name}.json"

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет данные таблицы в JSON-файл."""

    DATA_DIR.mkdir(exist_ok=True)

    filepath = DATA_DIR / f"{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
