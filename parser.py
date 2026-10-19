from datetime import datetime

LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "ERROR"}

def parse_line(line):
    parts = line.strip().split(" | ")
    if len(parts) != 5:
        return None

    ts_str, level, source, event_code, message = parts

    if level not in LEVELS:
        return None

    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except ValueError:
        return None

    if not source or not event_code or not message:
        return None

    return {
        "timestamp": ts,
        "level": level,
        "source": source,
        "event_code": event_code,
        "message": message
    }
