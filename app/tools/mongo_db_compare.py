import json
import os
from typing import List, Dict, Any
from flask import current_app

try:
    from pymongo import MongoClient
    from bson import ObjectId
    from bson.json_util import dumps as bson_dumps
except Exception:
    MongoClient = None  # handled in callers


def save_session(session_id: str, session: Dict[str, Any]) -> str:
    path = os.path.join(current_app.instance_path, 'mongo_compare_sessions')
    os.makedirs(path, exist_ok=True)
    fn = os.path.join(path, f'{session_id}.json')
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(session, f, default=str, indent=2)
    return fn


def load_session(session_id: str) -> Dict[str, Any]:
    fn = os.path.join(current_app.instance_path, 'mongo_compare_sessions', f'{session_id}.json')
    with open(fn, 'r', encoding='utf-8') as f:
        return json.load(f)


def connect(uri: str, timeout_ms: int = 5000):
    if MongoClient is None:
        raise RuntimeError('pymongo is not installed')
    # Create a client with a short serverSelectionTimeoutMS to fail fast
    client = MongoClient(uri, serverSelectionTimeoutMS=timeout_ms)
    # Attempt a server_info to validate connection
    client.server_info()
    return client


def list_databases(client) -> List[str]:
    return sorted(client.list_database_names())


def list_collections(client, db_name: str) -> List[str]:
    db = client[db_name]
    return sorted(db.list_collection_names())


def _load_docs_indexed(client, db_name: str, coll: str, limit: int = 1000) -> Dict[str, Any]:
    db = client[db_name]
    cursor = db[coll].find({}, limit=limit)
    out = {}
    for d in cursor:
        key = str(d.get('_id'))
        out[key] = d
    return out


def compare_collections(client_a, client_b, db_name_a: str, db_name_b: str, collections: List[str], limit: int = 1000):
    """Return a session dict with per-collection added/removed/modified counts and sample diffs.

    This is a lightweight implementation suitable for preview only. Accepts separate db names for A and B.
    """
    session = {'id': None, 'db_a': db_name_a, 'db_b': db_name_b, 'collections': {}}
    for coll in collections:
        try:
            a_docs = _load_docs_indexed(client_a, db_name_a, coll, limit)
        except Exception as e:
            a_docs = {}
        try:
            b_docs = _load_docs_indexed(client_b, db_name_b, coll, limit)
        except Exception as e:
            b_docs = {}

        a_keys = set(a_docs.keys())
        b_keys = set(b_docs.keys())
        added = sorted(list(a_keys - b_keys))
        removed = sorted(list(b_keys - a_keys))
        common = sorted(list(a_keys & b_keys))

        modified = []
        # simple field-level diff: show which top-level keys differ
        for k in common:
            da = a_docs.get(k)
            dbb = b_docs.get(k)
            if da != dbb:
                # prepare a small diff object: show both docs using bson json util
                modified.append({'_id': k, 'a': json.loads(bson_dumps(da)), 'b': json.loads(bson_dumps(dbb))})

        session['collections'][coll] = {
            'added_count': len(added),
            'removed_count': len(removed),
            'modified_count': len(modified),
            'added': added[:50],
            'removed': removed[:50],
            'modified': modified[:50]
        }
    return session
