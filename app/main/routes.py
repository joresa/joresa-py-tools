from flask import render_template, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app import db
from app.main import bp
from app.models import Tool, ToolUsage, User

@bp.route('/')
def index():
    return render_template('index.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    tools = Tool.query.filter_by(is_active=True).all()
    
    # Get user's recent activity
    recent_usage = ToolUsage.query.filter_by(user_id=current_user.id)\
        .order_by(desc(ToolUsage.timestamp))\
        .limit(5)\
        .all()
    
    return render_template('main/dashboard.html', 
                         title='Dashboard', 
                         tools=tools,
                         recent_usage=recent_usage)

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
