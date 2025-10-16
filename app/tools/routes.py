from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.tools import bp
from app.tools.forms import DiffForm
from app.models import Tool, ToolUsage, DiffHistory
import difflib
import html
import re

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
