def apply_filters(event, time_from, time_to, level, source):
    if time_from and event["timestamp"] < time_from:
        return False
    if time_to and event["timestamp"] >= time_to:
        return False
    if level and event["level"] != level:
        return False
    if source and event["source"] != source:
        return False
    return True
