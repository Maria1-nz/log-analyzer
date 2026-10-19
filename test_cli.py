import pytest
import json
import os
from datetime import datetime, timezone
from parser import parse_line
from filter import apply_filters
from aggregator import Aggregator
from output import save_to_json, save_to_csv
from cli import parse_date

def test_parse_valid_line():
    line = "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created"
    res = parse_line(line)
    assert res is not None
    assert res["level"] == "WARN"
    assert res["source"] == "auth-api"
    assert res["event_code"] == "AUTH_LOGIN_OK"

def test_parse_invalid_lines():
    assert parse_line("not-a-timestamp | ERROR | orders-api | ORDER_REJECTED | timestamp is invalid") is None
    assert parse_line("2026-09-01T00:08:59Z | NOTICE | gateway | HTTP_502 | unsupported level") is None
    assert parse_line("2026-09-01T00:08:59Z | INFO | auth-api | | missing event code") is None
    assert parse_line("too | short") is None

def test_parse_date():
    assert parse_date(None) is None
    dt = parse_date("2026-09-01T00:00:00Z")
    assert dt.year == 2026
    assert dt.month == 9

def test_filters():
    event = parse_line("2026-09-01T12:00:00Z | ERROR | payment-worker | PAYMENT_TIMEOUT | Timeout")
    
    assert apply_filters(event, None, None, "ERROR", "payment-worker") is True
    assert apply_filters(event, None, None, "INFO", None) is False
    assert apply_filters(event, None, None, None, "auth-api") is False
    
    time_from = parse_date("2026-09-01T13:00:00Z")
    time_to = parse_date("2026-09-01T11:00:00Z")
    assert apply_filters(event, time_from, None, None, None) is False
    assert apply_filters(event, None, time_to, None, None) is False
    assert apply_filters(event, time_from, time_to, None, None) is False

def test_aggregator_process():
    agg = Aggregator()
    valid_event = parse_line("2026-09-01T12:00:00Z | ERROR | auth-api | ERR_1 | Msg")
    
    agg.process_line(1, None, None, None, None, None)
    assert agg.invalid_lines == 1
    
    agg.process_line(2, valid_event, None, None, None, None)
    assert agg.valid_lines == 1
    assert agg.filtered_events == 1
    assert agg.levels_count["ERROR"] == 1
    assert agg.error_codes["ERR_1"] == 1
    
    summary = agg.get_summary()
    assert summary["total_lines"] == 2
    assert summary["top_error_codes"] == [("ERR_1", 1)]

def test_output_json(tmp_path):
    summary = {"total_lines": 10, "valid_lines": 8, "invalid_lines": 2, "invalid_line_numbers": [1, 2],
               "filtered_events": 8, "levels_count": {"INFO": 8}, "sources_count": {"api": 8},
               "top_error_codes": [("ERR", 1)]}
    file_path = tmp_path / "report.json"
    save_to_json(summary, file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data["total_lines"] == 10

def test_output_csv(tmp_path):
    summary = {"total_lines": 10, "valid_lines": 8, "invalid_lines": 2,
               "filtered_events": 8, "levels_count": {"INFO": 8}}
    file_path = tmp_path / "report.csv"
    save_to_csv(summary, file_path)
    
    assert os.path.exists(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Total Lines,10" in content

from output import print_summary
from cli import main
import sys

def test_print_summary(capsys):
    summary = {
        "total_lines": 10, "valid_lines": 8, "invalid_lines": 2, 
        "invalid_line_numbers": [1, 2], "filtered_events": 8, 
        "levels_count": {"INFO": 8}, "sources_count": {"api": 8},
        "top_error_codes": [("ERR", 1)]
    }
    print_summary(summary)
    captured = capsys.readouterr()
    assert "Всего строк: 10" in captured.out
    assert "Ошибочных: 2" in captured.out
    assert "ERR: 1" in captured.out

def test_main_file_not_found(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['cli.py', '--input', 'not_exist.log'])
    main()
    captured = capsys.readouterr()
    assert "Ошибка: файл not_exist.log не найден." in captured.out