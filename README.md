# Анализатор журналов событий (Log Analyzer CLI)

CLI-приложение для анализа, фильтрации и формирования сводки по журналам событий. Разработано в рамках практического задания.

## Установка и запуск
1. Перейдите в директорию проекта.
2. Создайте и активируйте виртуальное окружение: python3 -m venv venv и source venv/bin/activate
3. Установите зависимости: pip install -r requirements.txt

## Примеры запуска
1. Базовый запуск (вывод в консоль):
python3 cli.py --input logs_events_sample.log

2. Фильтрация по уровню и источнику:
python3 cli.py --input logs_events_sample.log --level ERROR --source payment-worker

3. Фильтрация по времени и сохранение в JSON:
python3 cli.py --input logs_events_sample.log --from "2026-09-01T00:00:00Z" --to "2026-09-02T00:00:00Z" --format json --output report.json

4. Сохранение в CSV с Top-10 ошибок:
python3 cli.py --input logs_events_sample.log --top 10 --format csv --output report.csv

