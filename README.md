# Primitive DB

Консольное приложение на Python, имитирующее работу с базой данных. Приложение позволяет создавать таблицы, добавлять, просматривать, обновлять и удалять записи. Данные сохраняются в JSON-файлах.

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Установка и запуск

Клонируйте репозиторий:

```bash
git clone https://github.com/mika-sova-05/project-2_sharipova_M26-555.git
```

Перейдите в директорию проекта:

```bash
cd project-2_sharipova_M26-555
```

Установите зависимости:

```bash
uv sync
```

Запустите приложение:

```bash
uv run database
```

## Работа с приложением

После запуска приложения отображается список доступных команд.

### Работа с таблицами

| Команда | Описание |
|---|---|
| `create_table <имя> <столбец1:тип> <столбец2:тип> ...` | Создать таблицу |
| `list_tables` | Показать список таблиц |
| `drop_table <имя>` | Удалить таблицу |
| `info <имя>` | Показать информацию о таблице |

Поддерживаемые типы данных: `int`, `str`, `bool`.

Пример создания таблицы:

```text
create_table users name:str age:int is_active:bool
```

### CRUD-операции

**Добавление записи:**

```text
insert into users values ("Anna", 25, True)
```

**Просмотр записей:**

```text
select from users
```

**Фильтрация записей:**

```text
select from users where age = 25
```

**Обновление записи:**

```text
update users set age = 26 where name = "Anna"
```

**Удаление записей:**

```text
delete from users where name = "Anna"
```

Перед удалением записей приложение запрашивает подтверждение пользователя.

### Общие команды

| Команда | Описание |
|---|---|
| `help` | Показать справочную информацию |
| `exit` | Выйти из приложения |

## Хранение данных

Приложение использует JSON-файлы для хранения информации:

- `db_meta.json` — метаданные таблиц: названия столбцов и их типы.
- `data/` — директория с JSON-файлами, содержащими записи таблиц.

## Декораторы и замыкания

В проекте реализованы следующие декораторы и замыкания:

- **`handle_db_errors`** — централизованно обрабатывает ошибки базы данных: `KeyError`, `ValueError` и `FileNotFoundError`.
- **`confirm_action(action_name)`** — запрашивает подтверждение пользователя перед удалением таблицы или записей.
- **`log_time`** — измеряет и выводит время выполнения функции с помощью `time.monotonic()`.
- **`create_cacher()`** — создаёт замыкание с внутренним словарём для кэширования результатов выполнения запросов `select`.

## Демонстрация работы

### Часть 2

[![asciicast](https://asciinema.org/a/xPsTYEVf7NL4p2Hx.svg)](https://asciinema.org/a/xPsTYEVf7NL4p2Hx)

### Часть 3

[![asciicast](https://asciinema.org/a/x92kJFOW2Fym6sG3.svg)](https://asciinema.org/a/x92kJFOW2Fym6sG3)

### Часть 4. Декораторы и замыкания

[![asciicast](https://asciinema.org/a/ygno4E92ZfvPsjpk.svg)](https://asciinema.org/a/ygno4E92ZfvPsjpk)
