# Выявление плагиата

Данный проект выполняется в рамках дисциплины *Программирование для лингвистов* на 4 курсе в НИУ ВШЭ - НН.

Цель - разработать инструмент, который позволяет проверять тексты на наличие плагиата. 

## Краткое описание проекта

1) Данные на вход: 2 текста (оригинальный и с плагиатом)
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

## Cтруктура проекта

```
revealing-plagiarism/
│
├── README.md
├── .gitignore
├── pyproject.toml
├── src/
│   ├── assets
│   ├── __init__.py 
│   ├── plagiarism-detector.py           
│   ├── report-maker.py          
│   └── main.py              
├── tests/
│   ├── __init__.py
│   ├── tbd.py
│   ├── tbd.py
│   └── ...
├── docs/
│   ├── index.rst
│   ├── tbd.py
│   ├── tbd.py
│   └── ...
└── ...
```
