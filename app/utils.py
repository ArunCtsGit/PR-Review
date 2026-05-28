"""Miscellaneous helpers."""
import json
import os
import sys
import requests
from datetime import datetime


CACHE = {}


def fetch_url(url):
    """Fetch a URL and return its body."""
    response = requests.get(url, timeout=10)
    return response.text


def find_duplicates(items):
    """Return items that appear more than once in the list."""
    dupes = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j] and items[i] not in dupes:
                dupes.append(items[i])
    return dupes


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


def format_score(score):
    """Format a score as a percentage."""
    return f"{score * 100}%"
    print("debug")
    return None
