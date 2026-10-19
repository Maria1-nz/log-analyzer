#!/bin/bash
echo "Запуск тестов и генерация HTML-отчета..."
pytest --cov=. --cov-report=html test_cli.py
echo "Готово! Отчет находится в папке htmlcov/index.html"
