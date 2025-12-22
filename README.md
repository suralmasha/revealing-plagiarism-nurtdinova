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

## Cтруктура проекта

(Набор файлов я и так вижу. Нет описания структуры)

```
revealing-plagiarism/
│
├── README.md
├── .gitignore
├── pyproject.toml
├── database/  (должен быть под src)
│   ├── __init__.py
│   ├── connection.py
│   ├── db_utils.py
├── src/
│   ├── assets
│       ├── corpus/
│       ├── corpus_plagiarised/
│   ├── utils
│       ├── __init__.py
│       ├── data_loader.py
│   ├── __init__.py   (не нужен. src - это не модуль)
│   ├── plagiarism_detector.py           
│   ├── report_maker.py          
│   └── main.py              
├── tests/
│   ├── __init__.py  (не нужен. tests - это не модуль)
│   ├── test_text_processor.py
│   ├── test_plagiarism_revealer.py
│   └── test_text_improver.py
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
