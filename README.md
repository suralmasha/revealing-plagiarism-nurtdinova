# Выявление плагиата

Данный проект выполняется в рамках дисциплины *Программирование для лингвистов* на 4 курсе в НИУ ВШЭ - НН.

Цель - разработать инструмент, который позволяет проверять тексты на наличие плагиата. 

## Краткое описание проекта

1) Данные на вход: корпус оригинальных текстов и текст с плагиатом
2) Вывод: степень схожести текстов (в %), отчет о совпадениях
3) Дополнительный вывод: изменение второго текста для увеличения процента уникальности

## Быстрый старт проекта

### Клонирование репозитория

```bash
git clone https://github.com/sofianurtdinova/revealing-plagiarism.git
```

### Создание виртуального окружения

```bash
python -m venv .venv
venv\Scripts\activate  # На macOS: source .venv/bin/activate
```

### Установка зависимостей

```bash
poetry install
```

### Запуск алгоритма

```bash
poetry run python src/main.py
```
* Если возникает ошибка с нахождением модулей, попробуйте указать PYTHONPATH и заново запустить программу:

```bash
$env:PYTHONPATH = "$pwd;" + $env:PYTHONPATH # на macOS: export PYTHONPATH=$pwd:$PYTHONPATH
```

## Cтруктура проекта

```
revealing-plagiarism/
│
├── README.md # Краткое описание проекта
├── .gitignore
├── pyproject.toml
├── database/ # Модуль для работы с БД
│   ├── __init__.py
│   ├── connection.py # Подключение к БД
│   ├── db_utils.py # Логика работы с БД
├── src/
│   ├── assets
│       ├── corpus/ # Корпус оригинальных текстов
│       ├── corpus_plagiarised/ # Корпус сплагиаченных текстов (для выбора)
│   ├── utils # Модуль для работы с синонимами
│       ├── __init__.py
│       ├── data_loader.py # Загрузка синонимов
│   ├── __init__.py 
│   ├── plagiarism_detector.py #           
│   ├── report_maker.py          
│   └── main.py              
├── tests/
│   ├── test_text_processor.py # Тесты класса для обработки текста
│   ├── test_plagiarism_revealer.py # Тесты класса для выявления плагиата
│   └── test_text_improver.py # Тесты класса для улучшения текста
├── .gitignore
├── .pre-commit-config.yaml
├── poetry.lock
├── pyproject.toml
├── README.md
└── 
```

## Пример работы

**Входные данные:**
* **Оригинал:** "Лингвистика исследует устройство языка. Ключевые области включают фонетику и синтаксис."
* **Проверка:** "Языкознание изучает структуру языка. Основные разделы охватывают фонетику и синтаксис."

**Результат:**

```text
--- Plagiarism Report ---
Overall Similarity: 20.10%
Cosine Metric: 0.20
Jaccard Metric: 0.20
Matching key concepts: фонетика, синтаксис, язык...

--- Improvement Report ---
Original similarity: 20.1%
New similarity: 12.6%
Improvement: 7.5%

Suggested text:
Языкознание изучает структуру речи. Основные разделы охватывают фонетику и синтаксис.
