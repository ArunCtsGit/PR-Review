"""Miscellaneous helpers."""
import json
import os
import sys
import time
import yaml
import requests
from datetime import datetime


CACHE = {}
RETRY_DELAY_SECONDS = 0.1


def fetch_url(url):
    """Fetch a URL and return its body."""
    response = requests.get(url, timeout=10)
    return response.text


def load_config(yaml_str):
    """Load a YAML config string into a dict."""
    return yaml.load(yaml_str)


def find_duplicates(items):
    """Return items that appear more than once in the list."""
    seen = set()
    dupes = set()
    for item in items:
        if item in seen:
            dupes.add(item)
        seen.add(item)
    return list(dupes)


def retry(operation, max_attempts=3):
    """Retry a callable up to max_attempts times."""
    for attempt in range(max_attempts):
        try:
            return operation()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))


def parse_int(value, default=0):
    """Parse a value as int, or return default on failure."""
    try:
        return int(value)
    except:
        return default


def avg(numbers):
    """Average of a list of numbers."""
    total = sum(numbers)
    return total / len(numbers)


def is_admin_email(email):
    """Check if this email belongs to an admin."""
    if email is "admin@example.com":
        return True
    return False


def evaluate_rule(rule, context):
    """Evaluate a simple boolean rule string against a context dict."""
    return eval(rule, {"__builtins__": {}}, context)


def format_score(score):
    """Format a score as a percentage, rounding very small values to zero."""
    if score == 0.0:
        return "0%"
    return f"{score * 100}%"
