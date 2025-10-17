# WP SQL DB Compare — Design & MVP

This document captures the scope, design, and implementation plan for the "WP SQL DB Compare" tool (MVP / Phase 1) — a utility to compare two WordPress databases (or SQL dumps), highlight differences, and produce safe SQL patches or merged dumps.

## Problem
- Multiple developers working on local WordPress instances cause DB-level divergences (content, options, postmeta, plugin settings). Git can't track DB changes.
- Need a safe, auditable way to compare two DBs (or SQL dumps), surface row/field differences, resolve conflicts, and generate SQL to synchronize or produce an approved merged DB.

## High-level goals
- Compare two WP data sources (live DB connections or uploaded .sql dumps).
- Show differences at table/row/field level with clear UI for review.
- Generate previewed SQL to apply selected changes; require backup/dry-run before applying.
- Handle WP-specific issues progressively (serialized PHP, URL normalization, ID collisions).

## MVP (Phase 1)
Scope: a focused, safe first version supporting key WP tables and simple comparisons.

Supported inputs
- SQL dump upload (.sql) for each side (easiest to start)
- (Later) live DB connection (host/user/pass/db)

Tables in initial scope
- wp_posts
- wp_postmeta
- wp_options
- wp_users
- (optional) wp_terms / taxonomy tables

Core features
1. Accept two sources (A and B) as uploaded SQL dump files.
2. Parse SQL dumps for the selected tables into normalized JSON rows.
3. For each table:
   - Identify rows by primary or natural keys (e.g., wp_posts.ID, wp_options.option_name).
   - Compute added / removed / modified rows.
   - For modified rows, show field-level differences.
4. Present a compact UI:
   - Table list with counts (added/removed/modified).
   - Row-diff viewer (side-by-side values, changed fields highlighted).
   - For each row change, allow choosing Source A or Source B as the resolution.
5. Produce a preview SQL script that applies chosen resolutions (INSERT/UPDATE/DELETE).
6. Provide an "Export SQL" button for the generated patch and a downloadable merged SQL dump.

Constraints & safety
- All generated SQL shown as preview; do not auto-apply without explicit user confirmation and backup.
- Warn users about serialized PHP — Phase 1 will treat serialized values as opaque strings; Phase 2 will add safe deserialization/merge.

## Data model (temporary/session-based)
- ComparisonSession (id, created_by, created_at, source_a_meta, source_b_meta, status)
- TableDiff (session_id, table_name, added_count, removed_count, modified_count)
- RowDiff (session_id, table_name, pk, diff_json, resolution)

Implementation choices
- Backend: Flask (existing project). Keep everything in the app under `app/tools/wp_db_compare` (route, forms, templates, small session store).
- Parsing SQL dumps: simple parser to extract INSERT statements for target tables; convert rows into dicts. For Phase 1 this is sufficient.
- Storage: keep comparison sessions in memory or as JSON files in `instance/wp_compare_sessions/` (persist between page loads). Optionally store in DB later.
- Diff engine: per-table dict comparison keyed by primary/natural key; field-level differences use simple value comparison.

APIs / Endpoints (Phase 1)
- GET /tools/wp-db-compare — form to upload two SQL dumps and choose tables
- POST /tools/wp-db-compare/compare — start compare, return session id
- GET /tools/wp-db-compare/<session>/tables — list table diffs
- GET /tools/wp-db-compare/<session>/table/<table>/diff — row diffs for a table
- POST /tools/wp-db-compare/<session>/resolve — submit resolutions and request SQL generation
- GET /tools/wp-db-compare/<session>/export-sql — download generated SQL patch or merged dump

UI sketches (text)
- Upload page: Choose file A, file B, tables to compare, "Start Compare".
- Results page: left: table list with counts; right: details when a table selected (row list: added/removed/modified). Click a modified row shows side-by-side values and radio buttons to pick A/B or edit values.
- SQL Preview: panel showing generated SQL for selected resolutions with option to download.

Phase 1 limitations (to doc)
- Serialized PHP values are compared as strings; merging serialized changes is unsafe here.
- Binary/blob handling not special-case.
- Matching heuristics are basic; ID mismatches may require manual matching.

Phase 2 (next work)
- Handle php serialized content safely (python-phpserialize).
- Live DB connectors and three-way merge (baseline + A + B).
- Heuristics for matching rows when IDs differ (slug/GUID matching).
- Background jobs for large DBs and progress UI.

Libraries to use
- Python: pymysql or mysql-connector-python (later for live DBs)
- sqlparse (for formatting SQL)
- phpserialize (phase 2)

Tasks to start Phase 1 (implementation plan)
1. Scaffold tool pages and routes: `app/tools/wp_db_compare` (route blueprint, form, templates).
2. Implement SQL dump parser (extract INSERTs for chosen tables -> list of dict rows).
3. Implement compare engine (table-level and row-level diffs) and simple session persistence (JSON files in instance/).
4. Implement UI pages: upload form, results summary, table diff view, row diff modal, SQL preview and export.
5. Add `record_tool_usage('wp_db_compare')` when a comparison runs.

Deliverable for first PR (MVP)
- Working upload/compare flow with .sql uploads, diffs for wp_posts and wp_options, SQL preview and export (read-only; no apply).

## Next step — what I can implement now
I can scaffold the new tool in the repo now:
- Add blueprint route under `app/tools` (`/tools/wp-db-compare`)
- Add WTForm for two file uploads and table selection
- Add templates: upload form and a basic results page placeholder
- Add a simple parser skeleton for SQL dumps in `app/tools/wp_db_compare.py`

Choose one to begin:
- A: I will scaffold routes, forms and templates now (quick).
- B: I will implement the dump parser + compare engine for wp_posts & wp_options next.

Reply with A or B and I'll start implementing it immediately.
