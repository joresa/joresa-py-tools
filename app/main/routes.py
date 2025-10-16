from flask import render_template, jsonify, request, redirect, flash, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from app import db
from app.main import bp
from app.models import Tool, ToolUsage, User, Category
from app.main.forms import CategoryForm, ToolAssignForm

@bp.route('/')
def index():
    return render_template('index.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    tools = Tool.query.filter_by(is_active=True).all()
    # Load categories with tools
    categories = Category.query.options(selectinload(Category.tools), selectinload(Category.children)).order_by(Category.display_name).all()
    
    # Get recent activity across users (most recent usages)
    recent_usage = ToolUsage.query.options(
        joinedload(ToolUsage.tool),
        joinedload(ToolUsage.user)
    ).order_by(desc(ToolUsage.timestamp)).limit(10).all()

    # Compute top 10 most used tools (by usage count)
    results = db.session.query(
        Tool,
        func.count(ToolUsage.id).label('count')
    ).join(ToolUsage).group_by(Tool.id).order_by(desc('count')).limit(10).all()
    most_used_tools_with_counts = [(r[0], r[1]) for r in results]
    
    return render_template('main/dashboard.html', 
                         title='Dashboard', 
                         tools=tools,
                         categories=categories,
                         recent_usage=recent_usage,
                         most_used_tools_with_counts=most_used_tools_with_counts)

@bp.route('/analytics')
@login_required
def analytics():
    return render_template('main/analytics.html', title='Analytics')

@bp.route('/api/analytics/most-used-tools')
@login_required
def api_most_used_tools():
    # Get most used tools in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    results = db.session.query(
        Tool.display_name,
        func.count(ToolUsage.id).label('count')
    ).join(ToolUsage).filter(
        ToolUsage.timestamp >= thirty_days_ago
    ).group_by(Tool.id).order_by(desc('count')).limit(10).all()
    
    return jsonify({
        'labels': [r[0] for r in results],
        'data': [r[1] for r in results]
    })

@bp.route('/api/analytics/usage-by-date')
@login_required
def api_usage_by_date():
    # Get usage by date for last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    results = db.session.query(
        func.date(ToolUsage.timestamp).label('date'),
        func.count(ToolUsage.id).label('count')
    ).filter(
        ToolUsage.timestamp >= thirty_days_ago
    ).group_by(func.date(ToolUsage.timestamp)).order_by('date').all()
    
    return jsonify({
        'labels': [str(r[0]) for r in results],
        'data': [r[1] for r in results]
    })

@bp.route('/api/analytics/usage-by-user')
@login_required
def api_usage_by_user():
    # Get top 10 users by usage
    results = db.session.query(
        User.username,
        func.count(ToolUsage.id).label('count')
    ).join(ToolUsage).group_by(User.id).order_by(desc('count')).limit(10).all()
    
    return jsonify({
        'labels': [r[0] for r in results],
        'data': [r[1] for r in results]
    })

@bp.route('/settings/categories')
@login_required
def categories_list():
    categories = Category.query.order_by(Category.display_name).all()
    return render_template('main/categories_list.html', title='Manage Categories', categories=categories)

@bp.route('/settings/categories/new', methods=['GET', 'POST'])
@login_required
def categories_new():
    form = CategoryForm()
    # populate parent choices
    parents = [(0, 'None')] + [(c.id, c.display_name or c.name) for c in Category.query.order_by(Category.display_name).all()]
    form.parent_id.choices = parents
    if form.validate_on_submit():
        cat = Category(name=form.name.data, display_name=form.display_name.data, parent_id=form.parent_id.data or None)
        db.session.add(cat)
        db.session.commit()
        flash('Category created', 'success')
        return redirect(url_for('main.categories_list'))
    return render_template('main/category_form.html', title='New Category', form=form)

@bp.route('/settings/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def categories_edit(id):
    cat = Category.query.get_or_404(id)
    form = CategoryForm(obj=cat)
    parents = [(0, 'None')] + [(c.id, c.display_name or c.name) for c in Category.query.order_by(Category.display_name).all() if c.id != id]
    form.parent_id.choices = parents
    if form.validate_on_submit():
        cat.name = form.name.data
        cat.display_name = form.display_name.data
        cat.parent_id = form.parent_id.data or None
        db.session.commit()
        flash('Category updated', 'success')
        return redirect(url_for('main.categories_list'))
    return render_template('main/category_form.html', title='Edit Category', form=form)

@bp.route('/settings/categories/<int:id>/delete', methods=['POST'])
@login_required
def categories_delete(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted', 'success')
    return redirect(url_for('main.categories_list'))

@bp.route('/settings/tools')
@login_required
def tools_manage():
    # list all tools and allow assigning category via form
    tools = Tool.query.order_by(Tool.display_name).all()
    categories = Category.query.order_by(Category.display_name).all()
    form = ToolAssignForm()
    form.category_id.choices = [('', 'Unassigned')] + [(c.id, c.display_name or c.name) for c in categories]
    return render_template('main/tools_manage.html', title='Manage Tools', tools=tools, categories=categories, form=form)

@bp.route('/settings/tools/<int:id>/assign', methods=['POST'])
@login_required
def tools_assign(id):
    tool = Tool.query.get_or_404(id)
    form = ToolAssignForm()
    categories = Category.query.order_by(Category.display_name).all()
    form.category_id.choices = [('', 'Unassigned')] + [(c.id, c.display_name or c.name) for c in categories]
    # Use request.form directly because form may not validate when empty
    cat_value = request.form.get('category_id')
    if cat_value:
        tool.category_id = int(cat_value)
    else:
        tool.category_id = None
    db.session.commit()
    flash('Tool assignment updated', 'success')
    return redirect(url_for('main.tools_manage'))
