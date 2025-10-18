from flask import render_template, redirect, url_for, flash, request, send_file, current_app, jsonify
from flask_login import login_required, current_user
from app import db
from app.tools import bp
from app.tools.forms import DiffForm
from app.models import Tool, ToolUsage, DiffHistory
import difflib
import html
import re
import os
import uuid
from werkzeug.utils import secure_filename
from app.tools.wp_db_compare import parse_sql_inserts, compare_tables, save_session, load_session, detect_tables_in_dump
from app.tools.rulecard import format_rulecard
from app.tools.forms import RuleCardForm

def record_tool_usage(tool_name):
    """Record that a tool was used"""
    tool = Tool.query.filter_by(name=tool_name).first()
    if tool:
        usage = ToolUsage(user_id=current_user.id, tool_id=tool.id)
        db.session.add(usage)
        db.session.commit()

def generate_diff_html(text1, text2, text1_name='Text 1', text2_name='Text 2'):
    """Generate HTML diff between two texts with line numbers for both files.

    Uses unified_diff output, parses hunk headers to track line numbers
    and renders each diff line with left/right line numbers and content.
    """
    # Split without keeping line endings to simplify numbering
    text1_lines = text1.splitlines()
    text2_lines = text2.splitlines()

    diff = difflib.unified_diff(text1_lines, text2_lines,
                                fromfile=text1_name,
                                tofile=text2_name,
                                lineterm='')

    html_lines = []
    from_ln = 0
    to_ln = 0

    hunk_re = re.compile(r"@@ -(?P<from_start>\d+)(?:,\d+)? \+(?P<to_start>\d+)(?:,\d+)? @@")

    for raw in diff:
        # raw is a line from unified diff (no trailing newline)
        if raw.startswith('+++') or raw.startswith('---'):
            html_lines.append(f'<div class="diff-header">{html.escape(raw)}</div>')
            continue

        if raw.startswith('@@'):
            m = hunk_re.search(raw)
            if m:
                from_ln = int(m.group('from_start'))
                to_ln = int(m.group('to_start'))
            html_lines.append(f'<div class="diff-range">{html.escape(raw)}</div>')
            continue

        # Prepare display numbers and content
        line_type = raw[:1]
        content = html.escape(raw[1:]) if len(raw) > 1 else ''

        if line_type == '+':
            # Added line: show right-side number
            ln_from = ''
            ln_to = to_ln
            to_ln += 1
            cls = 'diff-add'
            sign = '+'
        elif line_type == '-':
            # Removed line: show left-side number
            ln_from = from_ln
            ln_to = ''
            from_ln += 1
            cls = 'diff-remove'
            sign = '-'
        else:
            # Context line (also covers lines that don't start with +/-/ )
            ln_from = from_ln
            ln_to = to_ln
            from_ln += 1
            to_ln += 1
            cls = 'diff-context'
            sign = ' '

        # Render a line with two line-number columns and the content
        html_lines.append(
            '<div class="diff-line {cls}">'.format(cls=cls) +
            f'<span class="ln ln-from">{ln_from}</span>' +
            f'<span class="ln ln-to">{ln_to}</span>' +
            f'<span class="diff-marker">{html.escape(sign)}</span>' +
            f'<pre class="diff-content">{content}</pre>' +
            '</div>'
        )

    return '\n'.join(html_lines)

@bp.route('/diff', methods=['GET', 'POST'])
@login_required
def diff_checker():
    form = DiffForm()
    diff_result = None
    
    if form.validate_on_submit():
        text1 = form.text1.data
        text2 = form.text2.data
        text1_name = form.text1_name.data or 'Text 1'
        text2_name = form.text2_name.data or 'Text 2'
        
        # Generate diff
        diff_result = generate_diff_html(text1, text2, text1_name, text2_name)
        
        # Save to history
        history = DiffHistory(
            user_id=current_user.id,
            text1_name=text1_name,
            text2_name=text2_name,
            text1_content=text1,
            text2_content=text2,
            diff_result=diff_result
        )
        db.session.add(history)
        
        # Record tool usage
        record_tool_usage('diff_checker')
        
        db.session.commit()
        flash('Diff generated successfully!', 'success')
    
    return render_template('tools/diff_checker.html', 
                         title='Diff Checker', 
                         form=form,
                         diff_result=diff_result)

@bp.route('/diff/history')
@login_required
def diff_history():
    history = DiffHistory.query.filter_by(user_id=current_user.id)\
        .order_by(DiffHistory.timestamp.desc())\
        .all()
    return render_template('tools/diff_history.html', 
                         title='Diff History',
                         history=history)

@bp.route('/diff/history/<int:id>')
@login_required
def diff_history_detail(id):
    history = DiffHistory.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('tools/diff_history_detail.html',
                         title='Diff History Detail',
                         history=history)

@bp.route('/wp-db-compare')
@login_required
def wp_db_compare_index():
    # Render the interactive UI (moved from /wp-db-compare/ui)
    return render_template('tools/wp_db_compare/ui.html')


@bp.route('/wp-db-compare/compare', methods=['POST'])
@login_required
def wp_db_compare_compare():
    f_a = request.files.get('file_a')
    f_b = request.files.get('file_b')
    # If the user provided explicit table selections use them; otherwise we will detect
    tables = request.form.getlist('tables')
    if not f_a or not secure_filename(f_a.filename).lower().endswith('.sql'):
        flash('Please upload a valid .sql file for Source A', 'danger')
        return redirect(url_for('tools.wp_db_compare_index'))
    if not f_b or not secure_filename(f_b.filename).lower().endswith('.sql'):
        flash('Please upload a valid .sql file for Source B', 'danger')
        return redirect(url_for('tools.wp_db_compare_index'))

    text_a = f_a.read().decode('utf-8', errors='replace')
    text_b = f_b.read().decode('utf-8', errors='replace')

    # If tables weren't provided, detect from both dumps and present them
    from app.tools.wp_db_compare import detect_tables_in_dump
    if not tables:
        detected = set(detect_tables_in_dump(text_a)) | set(detect_tables_in_dump(text_b))
        # prefer common WP table names if present
        default_order = ['wp_posts', 'wp_postmeta', 'wp_options', 'wp_users']
        tables = [t for t in default_order if t in detected] + sorted([t for t in detected if t not in default_order])

    rows_a = parse_sql_inserts(text_a, tables)
    rows_b = parse_sql_inserts(text_b, tables)

    session_id = str(uuid.uuid4())
    session = {'id': session_id, 'tables': {}, 'meta': {'file_a': secure_filename(f_a.filename), 'file_b': secure_filename(f_b.filename)}, 'detected_tables': tables}
    for t in tables:
        added, removed, modified = compare_tables(rows_a.get(t, []), rows_b.get(t, []), t)
        session['tables'][t] = {
            'added_count': len(added),
            'removed_count': len(removed),
            'modified_count': len(modified),
            'added': added,
            'removed': removed,
            'modified': [ {'key': k, 'a': a, 'b': b, 'diffs': diffs} for (k,a,b,diffs) in modified ]
        }
    save_session(session_id, session)
    # record tool usage if available
    try:
        tool = Tool.query.filter_by(name='wp_db_compare').first()
        if tool:
            usage = ToolUsage(user_id=current_user.id, tool_id=tool.id)
            db.session.add(usage)
            db.session.commit()
    except Exception:
        pass
    return redirect(url_for('tools.wp_db_compare_result', session_id=session_id))


@bp.route('/wp-db-compare/result/<session_id>')
@login_required
def wp_db_compare_result(session_id):
    try:
        session = load_session(session_id)
    except FileNotFoundError:
        flash('Session not found', 'danger')
        return redirect(url_for('tools.wp_db_compare_index'))
    return render_template('tools/wp_db_compare/result.html', session=session)


@bp.route('/wp-db-compare/export/<session_id>')
@login_required
def wp_db_compare_export(session_id):
    try:
        session = load_session(session_id)
    except FileNotFoundError:
        flash('Session not found', 'danger')
        return redirect(url_for('tools.wp_db_compare_index'))
    out_path = os.path.join(current_app.instance_path, f'wp_compare_{session_id}.sql')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('-- WP DB Compare export (Phase 1)\n')
        f.write(f"-- Session: {session_id}\n")
        # Basic export: list modified counts as comments
        for t, info in session.get('tables', {}).items():
            f.write(f"-- Table {t}: +{info.get('added_count')} -{info.get('removed_count')} ~{info.get('modified_count')}\n")
    return send_file(out_path, as_attachment=True, download_name=f'wp_compare_{session_id}.sql')


@bp.route('/wp-db-compare/scan-db')
@login_required
def wp_db_compare_scan_db():
    """Return list of table names present in the application's configured database."""
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
    except Exception:
        tables = []
    return jsonify({'tables': sorted(tables)})

@bp.route('/wp-db-compare/ui')
@login_required
def wp_db_compare_ui():
    """Render the scaffolded UI page for WP DB Compare (preview/scaffold)."""
    return render_template('tools/wp_db_compare/ui.html')

@bp.route('/wp-db-compare/validate', methods=['POST'])
@login_required
def wp_db_compare_validate():
    """Validate uploaded SQL dump and return detected tables and any errors/warnings."""
    f = request.files.get('file')
    if not f:
        return jsonify({'valid': False, 'errors': ['No file uploaded']}), 200

    filename = secure_filename(f.filename or '')
    if not filename.lower().endswith('.sql'):
        return jsonify({'valid': False, 'errors': ['File does not have a .sql extension'], 'filename': filename}), 200

    try:
        text = f.read().decode('utf-8', errors='replace')
    except Exception as e:
        return jsonify({'valid': False, 'errors': [f'Could not read file: {e}'], 'filename': filename}), 200

    errors = []
    warnings = []

    # quick size checks (warn for very small or very large files)
    size = len(text.encode('utf-8'))
    if size < 100:
        errors.append('File content too small to be a SQL dump')
    if size > 25 * 1024 * 1024:
        warnings.append('File is large (>25MB); parsing may be slow')

    # quick heuristic: look for common SQL dump statements
    if not re.search(r"\b(INSERT\s+INTO|CREATE\s+TABLE|ALTER\s+TABLE|DROP\s+TABLE|LOCK\s+TABLES)\b", text, re.IGNORECASE):
        errors.append('No SQL statements detected (INSERT/CREATE/ALTER/DROP)')

    # detect table names
    try:
        tables = detect_tables_in_dump(text)
    except Exception as e:
        errors.append(f'Error detecting tables: {e}')
        tables = []

    if not tables:
        errors.append('No table names detected in the dump')

    # heuristic: check for unbalanced parentheses
    open_paren = text.count('(')
    close_paren = text.count(')')
    if open_paren != close_paren:
        errors.append(f'Unbalanced parentheses: found {open_paren} "(" vs {close_paren} ")"')

    # heuristics for unbalanced single quotes (basic: skip doubled single-quotes which represent escapes)
    def has_unbalanced_single_quotes(t: str) -> bool:
        i = 0
        unmatched = 0
        L = len(t)
        while i < L:
            ch = t[i]
            if ch == "'":
                # if next char is also a quote, it's an escaped quote '' -> skip both
                if i + 1 < L and t[i + 1] == "'":
                    i += 2
                    continue
                # otherwise toggle unmatched
                unmatched ^= 1
            i += 1
        return bool(unmatched)

    try:
        if has_unbalanced_single_quotes(text):
            errors.append('Possible unbalanced single quotes detected (unescaped or unmatched quotes)')
    except Exception:
        # non-fatal
        pass

    # try a lightweight parse for a few tables to ensure basic INSERT parsing works
    parsed_ok = False
    try:
        sample_tables = tables[:5]
        parsed = parse_sql_inserts(text[:200000], sample_tables)
        parsed_ok = any(parsed.get(t) for t in sample_tables)
        if not parsed_ok:
            warnings.append('No INSERT rows found in sample parse for the first detected tables')
    except Exception as e:
        errors.append(f'Parsing error: {e}')

    # Prepare response
    valid = len(errors) == 0
    response = {'valid': valid, 'filename': filename, 'tables': tables, 'parsed_sample': parsed_ok, 'errors': errors, 'warnings': warnings}
    return jsonify(response), 200

@bp.route('/rule-card-formatter', methods=['GET', 'POST'])
@login_required
def rule_card_formatter():
    form = RuleCardForm()
    result = None
    result_fmt = None
    if form.validate_on_submit():
        text = form.input_text.data or ''
        fmt = form.format_type.data or 'bulleted'
        result = format_rulecard(text, fmt)
        result_fmt = fmt
        # record usage
        try:
            tool = Tool.query.filter_by(name='rule_card_formatter').first()
            if tool:
                usage = ToolUsage(user_id=current_user.id, tool_id=tool.id)
                db.session.add(usage)
                db.session.commit()
        except Exception:
            pass
        # Save history for this formatted input
        try:
            from app.models import RuleCardHistory
            h = RuleCardHistory(user_id=current_user.id, format_type=fmt, input_text=text, result_text=result)
            db.session.add(h)
            db.session.commit()
        except Exception:
            pass
    return render_template('tools/rule_card_formatter.html', form=form, result=result, result_fmt=result_fmt)

@bp.route('/rule-card-formatter/history')
@login_required
def rule_card_history():
    from app.models import RuleCardHistory
    history = RuleCardHistory.query.filter_by(user_id=current_user.id).order_by(RuleCardHistory.timestamp.desc()).all()
    return render_template('tools/rule_card_history.html', title='Rule Card History', history=history)

@bp.route('/rule-card-formatter/history/<int:id>')
@login_required
def rule_card_history_detail(id):
    from app.models import RuleCardHistory
    h = RuleCardHistory.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('tools/rule_card_history_detail.html', title='Rule Card History Detail', history=h)

@bp.route('/mongo-db-compare')
@login_required
def mongo_db_compare_index():
    from app.tools.forms import MongoCompareForm
    form = MongoCompareForm()
    return render_template('tools/mongo_db_compare/index.html', form=form)


@bp.route('/mongo-db-compare/discover', methods=['POST'])
@login_required
def mongo_db_compare_discover():
    """Discover databases for a given URI (POST body: {uri, side: 'A'|'B'})"""
    data = request.json or {}
    uri = data.get('uri')
    if not uri:
        return jsonify({'ok': False, 'error': 'No URI provided'}), 400
    try:
        from app.tools.mongo_db_compare import connect, list_databases
        client = connect(uri)
        dbs = list_databases(client)
        return jsonify({'ok': True, 'dbs': dbs}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 200


@bp.route('/mongo-db-compare/collections', methods=['POST'])
@login_required
def mongo_db_compare_collections():
    """Return collections for a given URI and database (POST body: {uri, db_name})"""
    data = request.json or {}
    uri = data.get('uri')
    db_name = data.get('db_name')
    if not uri or not db_name:
        return jsonify({'ok': False, 'error': 'Missing uri or db_name'}), 400
    try:
        from app.tools.mongo_db_compare import connect, list_collections
        client = connect(uri)
        cols = list_collections(client, db_name)
        return jsonify({'ok': True, 'collections': cols}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 200


# Update compare route signature to accept db_name_a and db_name_b
@bp.route('/mongo-db-compare/compare', methods=['POST'])
@login_required
def mongo_db_compare_compare():
    from app.tools.forms import MongoCompareForm
    from app.tools.mongo_db_compare import connect, list_collections, compare_collections, save_session
    form = MongoCompareForm()
    # form now expected to provide uri_a, uri_b, db_a, db_b, collections string
    if not form.validate_on_submit():
        flash('Please provide both Mongo URIs and database names', 'danger')
        return redirect(url_for('tools.mongo_db_compare_index'))

    uri_a = form.uri_a.data.strip()
    uri_b = form.uri_b.data.strip()
    db_a = request.form.get('db_a', '').strip()
    db_b = request.form.get('db_b', '').strip()
    coll_input = form.collections.data or ''
    try:
        limit = int(form.doc_limit.data)
    except Exception:
        limit = 1000

    collections = [c.strip() for c in coll_input.split(',') if c.strip()] if coll_input else None

    # Connect to both
    try:
        client_a = connect(uri_a)
    except Exception as e:
        flash(f'Could not connect to Source A: {e}', 'danger')
        return redirect(url_for('tools.mongo_db_compare_index'))
    try:
        client_b = connect(uri_b)
    except Exception as e:
        flash(f'Could not connect to Source B: {e}', 'danger')
        return redirect(url_for('tools.mongo_db_compare_index'))

    # If collections None, list collections from both dbs and take intersection
    if collections is None:
        cols_a = set(list_collections(client_a, db_a))
        cols_b = set(list_collections(client_b, db_b))
        collections = sorted(list(cols_a & cols_b))

    session = compare_collections(client_a, client_b, db_a, db_b, collections, limit=limit)
    import uuid
    session_id = str(uuid.uuid4())
    session['id'] = session_id
    session['meta'] = {'db_a': db_a, 'db_b': db_b, 'collections': collections, 'limit': limit}
    save_session(session_id, session)

    # record usage if tool exists
    try:
        tool = Tool.query.filter_by(name='mongo_db_compare').first()
        if tool:
            usage = ToolUsage(user_id=current_user.id, tool_id=tool.id)
            db.session.add(usage)
            db.session.commit()
    except Exception:
        pass

    return redirect(url_for('tools.mongo_db_compare_result', session_id=session_id))


@bp.route('/mongo-db-compare/result/<session_id>')
@login_required
def mongo_db_compare_result(session_id):
    from app.tools.mongo_db_compare import load_session
    try:
        session = load_session(session_id)
    except FileNotFoundError:
        flash('Session not found', 'danger')
        return redirect(url_for('tools.mongo_db_compare_index'))
    return render_template('tools/mongo_db_compare/result.html', session=session)


@bp.route('/mongo-db-compare/preview/<session_id>')
@login_required
def mongo_db_compare_preview(session_id):
    # Simple preview endpoint that returns generated pymongo bulk op code for download or inspection
    from app.tools.mongo_db_compare import load_session
    try:
        session = load_session(session_id)
    except FileNotFoundError:
        return jsonify({'error': 'session not found'}), 404
    # For now return JSON of session (preview shown in template)
    return render_template('tools/mongo_db_compare/preview.html', session=session)
