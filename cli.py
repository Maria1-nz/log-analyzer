import argparse
from datetime import datetime
from parser import parse_line
from aggregator import Aggregator
from output import print_summary, save_to_json, save_to_csv

def parse_date(date_str):
    if not date_str:
        return None
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

def main():
    arg_parser = argparse.ArgumentParser(description="Log Analyzer")
    arg_parser.add_argument("--input", required=True, help="Путь к файлу лога")
    arg_parser.add_argument("--from", dest="time_from", help="Начало интервала (ISO 8601)")
    arg_parser.add_argument("--to", dest="time_to", help="Конец интервала (исключительно)")
    arg_parser.add_argument("--level", help="Фильтр по уровню")
    arg_parser.add_argument("--source", help="Фильтр по источнику")
    arg_parser.add_argument("--top", type=int, default=5, help="Топ-N кодов ошибок")
    arg_parser.add_argument("--format", choices=["json", "csv"], help="Формат отчета")
    arg_parser.add_argument("--output", help="Путь сохранения файла")

    args = arg_parser.parse_args()

    time_from = parse_date(args.time_from)
    time_to = parse_date(args.time_to)

    aggregator = Aggregator()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                parsed = parse_line(line)
                aggregator.process_line(
                    line_num, parsed, 
                    time_from, time_to, 
                    args.level, args.source
                )
    except FileNotFoundError:
        print(f"Ошибка: файл {args.input} не найден.")
        return

    summary = aggregator.get_summary(args.top)
    print_summary(summary)

    if args.format and args.output:
        if args.format == "json":
            save_to_json(summary, args.output)
        elif args.format == "csv":
            save_to_csv(summary, args.output)
        print(f"\nОтчет сохранен в {args.output}")

if __name__ == "__main__":
    main()
