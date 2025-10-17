import os
import re
import csv
import json
from typing import List, Dict, Tuple

SQL_INSERT_RE = re.compile(r"INSERT INTO [`\"]?(?P<table>\w+)[`\"]?\s*\((?P<cols>[^)]+)\)\s*VALUES\s*(?P<values>.+);", re.IGNORECASE | re.DOTALL)
VALUES_RE = re.compile(r"\(([^)]*)\)(?:,\s*)?", re.DOTALL)

# Simple SQL value unquote/unescape for basic SQL dumps
def _unquote_sql_value(val: str):
    val = val.strip()
    if val == 'NULL':
        return None
    if val.startswith("'") and val.endswith("'"):
        # unescape single quotes
        inner = val[1:-1]
        return inner.replace("''", "'")
    if val.startswith('"') and val.endswith('"'):
        inner = val[1:-1]
        return inner.replace('""', '"')
    # numeric?
    if re.match(r'^-?\d+(\.\d+)?$', val):
        if '.' in val:
            return float(val)
        return int(val)
    return val


def parse_sql_inserts(sql_text: str, tables: List[str]) -> Dict[str, List[Dict[str, object]]]:
    """Parse INSERT INTO statements for the given tables from a SQL dump text.

    Returns a dict: {table_name: [row_dict, ...]}
    """
    result = {t: [] for t in tables}
    # Normalize newlines
    # remove line comments -- simplistic
    cleaned = re.sub(r"--.*\n", "\n", sql_text)
    # collapse multi-line INSERTs
    # Find all INSERT INTO ...; blocks
    for m in SQL_INSERT_RE.finditer(cleaned):
        table = m.group('table')
        if table not in tables:
            continue
        cols = [c.strip().strip('`"') for c in m.group('cols').split(',')]
        values_blob = m.group('values')
        for vmatch in VALUES_RE.finditer(values_blob):
            values_raw = vmatch.group(1)
            # split respecting commas inside quotes - rudimentary
            parts = []
            cur = ''
            in_quote = False
            quote_char = None
            for ch in values_raw:
                if ch in "'\"":
                    if not in_quote:
                        in_quote = True
                        quote_char = ch
                        cur += ch
                        continue
                    elif quote_char == ch:
                        cur += ch
                        in_quote = False
                        quote_char = None
                        continue
                if ch == ',' and not in_quote:
                    parts.append(cur.strip())
                    cur = ''
                else:
                    cur += ch
            if cur.strip() != '':
                parts.append(cur.strip())
            # map cols -> parts
            row = {}
            for col, part in zip(cols, parts):
                row[col] = _unquote_sql_value(part)
            result[table].append(row)
    return result


def build_table_key(table: str, row: Dict[str, object]) -> Tuple:
    """Return a tuple key for the row based on the table default PK heuristics.

    For Phase 1, use common WP keys:
    - wp_posts -> ID
    - wp_options -> option_name
    - wp_postmeta -> meta_id
    - wp_users -> ID
    """
    table_lower = table.lower()
    if table_lower.endswith('wp_posts') or table_lower == 'wp_posts' or table_lower.endswith('.posts'):
        return (row.get('ID'),)
    if table_lower.endswith('wp_options') or table_lower == 'wp_options':
        return (row.get('option_name'),)
    if table_lower.endswith('wp_postmeta') or table_lower == 'wp_postmeta':
        return (row.get('meta_id'),)
    if table_lower.endswith('wp_users') or table_lower == 'wp_users':
        return (row.get('ID'),)
    # fallback: use primary first column
    if len(row.keys()) > 0:
        return (next(iter(row.keys())),)
    return tuple()


def compare_tables(rows_a: List[Dict[str, object]], rows_b: List[Dict[str, object]], table: str):
    """Compare two row lists and return (added, removed, modified) where:
    - added: rows present in B not in A
    - removed: rows present in A not in B
    - modified: list of tuples (key, row_a, row_b, field_diffs)
    """
    dict_a = {build_table_key(table, r): r for r in rows_a}
    dict_b = {build_table_key(table, r): r for r in rows_b}
    keys_a = set(dict_a.keys())
    keys_b = set(dict_b.keys())
    added_keys = keys_b - keys_a
    removed_keys = keys_a - keys_b
    common = keys_a & keys_b
    added = [dict_b[k] for k in added_keys]
    removed = [dict_a[k] for k in removed_keys]
    modified = []
    for k in common:
        ra = dict_a[k]
        rb = dict_b[k]
        diffs = {}
        for col in set(list(ra.keys()) + list(rb.keys())):
            if ra.get(col) != rb.get(col):
                diffs[col] = {'a': ra.get(col), 'b': rb.get(col)}
        if diffs:
            modified.append((k, ra, rb, diffs))
    return added, removed, modified


# Session persistence helpers
SESSION_DIR = os.path.join(os.getcwd(), 'instance', 'wp_compare_sessions')


def save_session(session_id: str, data: dict):
    os.makedirs(SESSION_DIR, exist_ok=True)
    path = os.path.join(SESSION_DIR, f"{session_id}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, default=str)


def load_session(session_id: str) -> dict:
    path = os.path.join(SESSION_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def detect_tables_in_dump(sql_text: str) -> List[str]:
    """Detect table names referenced in a SQL dump (INSERT INTO and CREATE TABLE).

    Returns a sorted list of unique table names found.
    """
    tables = set()
    # find INSERT INTO <table>
    for m in re.finditer(r"INSERT\s+INTO\s+[`\"]?(?P<table>\w+)[`\"]?", sql_text, re.IGNORECASE):
        tables.add(m.group('table'))
    # find CREATE TABLE `name`
    for m in re.finditer(r"CREATE\s+TABLE\s+[`\"]?(?P<table>\w+)[`\"]?", sql_text, re.IGNORECASE):
        tables.add(m.group('table'))
    return sorted(tables)
