from collections import Counter
from filter import apply_filters

class Aggregator:
    def __init__(self):
        self.total_lines = 0
        self.valid_lines = 0
        self.invalid_lines = 0
        self.invalid_line_numbers = []
        self.filtered_events = 0
        self.levels_count = Counter()
        self.sources_count = Counter()
        self.error_codes = Counter()

    def process_line(self, line_num, parsed_event, time_from, time_to, level, source):
        self.total_lines += 1
        
        if parsed_event is None:
            self.invalid_lines += 1
            self.invalid_line_numbers.append(line_num)
            return

        self.valid_lines += 1
        
        if apply_filters(parsed_event, time_from, time_to, level, source):
            self.filtered_events += 1
            self.levels_count[parsed_event["level"]] += 1
            self.sources_count[parsed_event["source"]] += 1
            
            if parsed_event["level"] in ("ERROR", "WARN"):
                self.error_codes[parsed_event["event_code"]] += 1

    def get_summary(self, top_n=5):
        return {
            "total_lines": self.total_lines,
            "valid_lines": self.valid_lines,
            "invalid_lines": self.invalid_lines,
            "invalid_line_numbers": self.invalid_line_numbers,
            "filtered_events": self.filtered_events,
            "levels_count": dict(self.levels_count),
            "sources_count": dict(self.sources_count),
            "top_error_codes": self.error_codes.most_common(top_n)
        }
