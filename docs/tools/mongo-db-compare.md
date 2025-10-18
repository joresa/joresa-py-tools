# Mongo DB Compare — Design & Phase 1 (Preview-only)

This document captures scope, architecture and an implementation plan for a MongoDB comparison tool that mirrors the WP SQL DB Compare tool but operates on two MongoDB sources (URI A and URI B). Phase 1 focuses on read-only comparison and preview of upsert operations; Phase 2 will add execution (A→B / B→A) with safeguards.

## Goals
- Compare two MongoDB sources given connection URIs.
- Enumerate databases and collections (or allow the user to pick a single database/collection list).
- Compute collection-level diffs (added/removed/modified documents) using `_id` as the primary key.
- Provide per-document field-level diffs and a preview of bulk upsert operations (UpdateOne with upsert=True).
- Keep all operations preview-only in Phase 1 (no writes).

## Security & safety
- Do not persist credentials in VCS. Store only in-session (server memory or ephemeral JSON in instance/) and clear after session expiry.
- Require explicit user confirmation before any write action (Phase 2).
- Provide limits (max docs per collection) and a default sample-size to prevent accidental full scans.
- Use connection timeouts and validate URIs before running heavy operations.

## Supported inputs
- MongoDB connection URIs (mongodb:// or mongodb+srv://) for Source A and Source B.
- Database selection (pick a database present on the cluster).
- Collection selection (choose collections or "all" — default to enumerated user-visible collections).
- Document limit per-collection (default: 1000, configurable per-compare).

## Primary key
- Use `_id` as the primary identifier by default for all collections (per your decision).

## Output & UX (Phase 1)
- Session-based workflow with a session id and an expiration (e.g., 24 hours):
  - Upload/Connect page: two fields for Mongo URIs, select DB, select collections, doc limit.
  - Compare run page: shows collection list with counts of added/removed/modified.
  - Collection detail page: list of document diffs (added/removed/modified). Click a modified doc to view field-level differences side-by-side.
  - SQL-equivalent preview: show generated pymongo bulk operations (UpdateOne/ReplaceOne) for the selected resolutions. Present these as previewed Python (pymongo) or JavaScript (mongo shell) code the user could run locally.

## Data model (session-based)
- CompareSession: {id, created_by, created_at, srcA_uri_redacted, srcB_uri_redacted, db_name, collections, status, meta}
- CollectionDiff: {session_id, collection_name, added_count, removed_count, modified_count, sample_docs}
- DocDiff: {session_id, collection_name, _id, side_a_doc, side_b_doc, field_diffs}

Sessions should be persisted as ephemeral JSON files in `instance/mongo_compare_sessions/` so results survive a restart for a short time.

## API / Endpoints (Phase 1)
- GET /tools/mongo-db-compare — form with URI A, URI B, DB select, collections select, doc limit
- POST /tools/mongo-db-compare/compare — starts the compare, returns session id
- GET /tools/mongo-db-compare/<session>/collections — list collection diffs
- GET /tools/mongo-db-compare/<session>/collection/<name>/diff — row/document diffs (paginated)
- GET /tools/mongo-db-compare/<session>/collection/<name>/doc/<id>/diff — field-level diff for a single document
- GET /tools/mongo-db-compare/<session>/preview-upsert — generate preview of bulk upsert operations for chosen docs
- (Phase 2) POST /tools/mongo-db-compare/<session>/execute-upsert — executes upserts (requires confirmation)

## Diff algorithm (Phase 1)
- For each collection:
  1. Load documents from A and B limited by doc-limit (or sample if large).
  2. Index each set by `_id` (using stringified `_id` for keys).
  3. Compute sets: added = ids in A not in B, removed = ids in B not in A, common = intersection.
  4. For `common`, compute `field_diffs` using a shallow-to-moderate nested dict comparator (nested keys compared recursively). Optionally use `deepdiff` for richer diffs.
  5. For preview, generate UpdateOne operations that replace fields from chosen source, or a ReplaceOne(upsert=True) if desired.

Notes:
- Binary/BSON types and ObjectId should be displayed as readable strings (ObjectId(...)) in previews.
- Preserve nested structure: diffs should highlight changed nested fields.

## Implementation plan (tasks)
Phase 1 (preview only):
1. Scaffold blueprint under `app/tools/mongo_db_compare` with routes, forms and templates.
2. Add WTForm `MongoCompareForm` (URI A, URI B, DB name, collections multi-select, doc_limit).
3. Implement `app/tools/mongo_db_compare.py`:
   - `connect(uri)` helper that returns a `pymongo.MongoClient` wrapped with timeout and error handling.
   - `list_dbs_and_collections(client)` helper.
   - `compare_collections(srcA_client, srcB_client, db_name, collection, limit)` that returns CollectionDiff and sample DocDiffs.
   - `generate_upsert_preview(doc_diffs, chosen_source)` that emits Python (pymongo) bulk operations as text.
4. Session storage: write JSON session files to `instance/mongo_compare_sessions/<session>.json` and expose APIs to load/save session state.
5. Implement templates:
   - `mongo_db_compare.html` (form)
   - `mongo_db_compare_results.html` (collection list and counts)
   - `mongo_db_compare_collection_diff.html` (per-collection diffs, doc list, diff modal)
   - `mongo_db_compare_preview.html` (preview of pymongo bulk ops)
6. Add usage recording (record_tool_usage('mongo_db_compare')) on compare runs.
7. Add unit tests for `compare_collections` on small synthetic datasets.

Phase 2 (execute / sync):
- Add execute endpoint that runs `bulk_write` on the target with dry-run and confirm steps.
- Add rate limits, operation chunking, and optional transaction support (if both clusters support transactions).
- Add audit log of executed operations and rollback guidance.

## Dependencies
- pymongo
- dnspython (for mongodb+srv URIs)
- deepdiff (optional, for nicer diffs)

Add to `requirements.txt` when ready.

## UX recommendations
- Default to `_id` as the primary key and show a per-collection toggle when users supply a different natural key.
- For large collections, use sampling or pagination and clearly display that the operation is partial.
- Offer export of previewed operations as a `.py` or `.js` script that users can run locally against their target cluster.

## Next steps (short-term)
- I will scaffold the blueprint, forms and templates (minimal), wire a basic compare implementation using `_id`, and add session persistence. This will produce a preview-only working flow.

---

Document created for immediate reference during implementation and future Phase 2 work.
