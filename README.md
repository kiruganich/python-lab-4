# Система управления библиотекой - Лабораторная работа №4

## Описание проекта

Проект реализует **систему управления библиотекой** с пользовательскими коллекциями и псевдослучайной симуляцией событий.

### Основной функционал:
- **Две пользовательские коллекции**: ListCollection (через композицию) и DictCollection (индексирование)
- **Полная поддержка магических методов**: `__getitem__`, `__iter__`, `__len__`, `__contains__`, `__repr__`
- **Иерархия классов**: базовый класс Book и его расширение (BookCollection, IndexDict, Library)
- **Поиск и индексирование**: по ISBN, автору, году, жанру
- **Псевдослучайная симуляция**: 6 типов событий, воспроизводимость через seed
- **Логирование**: всех операций и событий симуляции
- **Полное покрытие тестами**


## Структура проекта

```
library-system/
│
├── src/                           # Основная логика
│   ├── __init__.py               # Пакет src
│   ├── constants.py              # Константы проекта
│   ├── models.py                 # Модели (Book, BookCollection, IndexDict, Library)
│   ├── simulation.py             # Симуляция событий
│   └── logger_config.py          # Конфигурация логирования
│
├── tests/                        # Тесты
│   ├── __init__.py              # Пакет tests
│   └── test.py                  # Все тесты (pytest)
│
├── main.py                       # Точка входа в приложение
├── requirements.txt              # Зависимости
├── README.md                     # Этот файл
└── .gitignore                    # Игнорирование файлов Git
```

---

## Установка и запуск

### 1. Требования
- **Python 3.8+**
- **pytest 7.0.0+**

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Запуск симуляции

**Базовый запуск (20 шагов со случайным seed):**
```bash
python main.py
```

**С указанным количеством шагов:**
```bash
python main.py 50
```

**С воспроизводимым seed (для одинаковых результатов):**
```bash
python main.py 30 42
```

**Справка:**
```bash
python main.py --help
python main.py -h
```

### 4. Запуск тестов

**Все тесты:**
```bash
pytest tests/test.py
```

**С подробным выводом:**
```bash
pytest tests/test.py -v
```

**Только определённый класс тестов:**
```bash
pytest tests/test.py::TestBook -v
```


## Пример работы

```
======================================================================
LIBRARY SIMULATION: 20 steps
======================================================================

[Step 1] Added new book: Foundation by Isaac Asimov (1951) - Science [ISBN: ISBN-001000]
[Step 2] Search by author 'Carl Sagan': found 0 book(s)
[Step 3] Added new book: Cosmos by Carl Sagan (1980) - Science [ISBN: ISBN-001001]
[Step 4] Search by ISBN 'ISBN-999999': NOT FOUND (expected behavior)
[Step 5] Search by genre 'Science': found 2 book(s)
...

======================================================================
FINAL STATISTICS:
======================================================================
Total books: 15
Unique authors: 6
Year range: 1950 - 2024
Genres: Fiction, Science, History, Technology, Biography
======================================================================
```


## Особенности реализации

### 1. Композиция в BookCollection
```python
class BookCollection:
    def __init__(self):
        self._books: List[Book] = []  # Композиция
```

### 2. Магические методы для поддержки Python API
```python
# Позволяет использовать:
len(collection)              # __len__
for book in collection:      # __iter__
book = collection[0]         # __getitem__
books = collection[1:3]      # __getitem__ со срезом (работает через __getitem__)
book in collection           # __contains__
```

### 3. IndexDict автоматически синхронизируется
```python
# При добавлении книги в Library:
library.add_book(book)
# - Обновляется BookCollection
# - Обновляется IndexDict (все три индекса)
```

### 4. Воспроизводимая симуляция
```python
# Одинаковый seed → одинаковые события
run_simulation(steps=20, seed=42)  # Первый раз
run_simulation(steps=20, seed=42)  # Второй раз — идентичны
```



## Зависимости

```
Python 3.8+
pytest>=7.0.0
```

