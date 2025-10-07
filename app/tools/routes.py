from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.tools import bp
from app.tools.forms import DiffForm
from app.models import Tool, ToolUsage, DiffHistory
import difflib
import html

def record_tool_usage(tool_name):
    """Record that a tool was used"""
    tool = Tool.query.filter_by(name=tool_name).first()
    if tool:
        usage = ToolUsage(user_id=current_user.id, tool_id=tool.id)
        db.session.add(usage)
        db.session.commit()

def generate_diff_html(text1, text2, text1_name='Text 1', text2_name='Text 2'):
    """Generate HTML diff between two texts"""
    text1_lines = text1.splitlines(keepends=True)
    text2_lines = text2.splitlines(keepends=True)
    
    diff = difflib.unified_diff(text1_lines, text2_lines, 
                                fromfile=text1_name, 
                                tofile=text2_name,
                                lineterm='')
    
    html_lines = []
    for line in diff:
        line = html.escape(line)
        if line.startswith('+++') or line.startswith('---'):
            html_lines.append(f'<div class="diff-header">{line}</div>')
        elif line.startswith('@@'):
            html_lines.append(f'<div class="diff-range">{line}</div>')
        elif line.startswith('+'):
            html_lines.append(f'<div class="diff-add">{line}</div>')
        elif line.startswith('-'):
            html_lines.append(f'<div class="diff-remove">{line}</div>')
        else:
            html_lines.append(f'<div class="diff-context">{line}</div>')
    
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
