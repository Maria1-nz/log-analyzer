import json
import csv

def print_summary(summary):
    print(f"Всего строк: {summary['total_lines']}")
    print(f"Корректных: {summary['valid_lines']}")
    print(f"Ошибочных: {summary['invalid_lines']}")
    if summary['invalid_line_numbers']:
        print(f"Номера ошибочных строк (первые 10): {summary['invalid_line_numbers'][:10]}")
        
    print(f"Событий после фильтрации: {summary['filtered_events']}")
    
    print("\nСводка по уровням:")
    for level, count in summary['levels_count'].items():
        print(f"  {level}: {count}")
        
    print("\nTop-N кодов ошибок (WARN/ERROR):")
    for code, count in summary['top_error_codes']:
        print(f"  {code}: {count}")

def save_to_json(summary, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)

def save_to_csv(summary, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Lines", summary['total_lines']])
        writer.writerow(["Valid Lines", summary['valid_lines']])
        writer.writerow(["Invalid Lines", summary['invalid_lines']])
        writer.writerow(["Filtered Events", summary['filtered_events']])
        for level, count in summary['levels_count'].items():
            writer.writerow([f"Level: {level}", count])
