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
    
    # Quick stats for the dashboard
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Total launches this week
    total_launches = ToolUsage.query.filter(ToolUsage.timestamp >= seven_days_ago).count()
    
    # Most used tool this week
    most_used = db.session.query(
        Tool.display_name,
        func.count(ToolUsage.id).label('count')
    ).join(ToolUsage).filter(
        ToolUsage.timestamp >= seven_days_ago
    ).group_by(Tool.id).order_by(desc('count')).first()
    
    # Average daily logins (unique users per day)
    unique_users_per_day = db.session.query(
        func.date(ToolUsage.timestamp).label('date'),
        func.count(func.distinct(ToolUsage.user_id)).label('users')
    ).filter(
        ToolUsage.timestamp >= seven_days_ago
    ).group_by(func.date(ToolUsage.timestamp)).all()
    
    avg_daily_logins = sum([r[1] for r in unique_users_per_day]) / max(len(unique_users_per_day), 1)
    
    # Active users this week
    active_users = db.session.query(func.count(func.distinct(ToolUsage.user_id))).filter(
        ToolUsage.timestamp >= seven_days_ago
    ).scalar() or 0
    
    # Average daily usage
    days_count = len(set([r[0] for r in unique_users_per_day])) or 1
    avg_daily_usage = total_launches / days_count
    
    quick_stats = {
        'most_used_tool': most_used[0] if most_used else 'N/A',
        'most_used_count': most_used[1] if most_used else 0,
        'total_launches': total_launches,
        'avg_daily_logins': round(avg_daily_logins, 1),
        'active_users': active_users,
        'avg_daily_usage': round(avg_daily_usage, 1),
        'available_tools': len(tools)
    }
    
    return render_template('main/dashboard.html', 
                         title='Dashboard', 
                         tools=tools,
                         recent_usage=recent_usage,
                         quick_stats=quick_stats)

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

@bp.route('/api/analytics/usage-by-department')
@login_required
def api_usage_by_department():
    # Get usage by department
    results = db.session.query(
        User.department,
        func.count(ToolUsage.id).label('count')
    ).join(ToolUsage).group_by(User.department).order_by(desc('count')).all()
    
    return jsonify({
        'labels': [r[0] for r in results],
        'data': [r[1] for r in results]
    })

@bp.route('/api/analytics/quick-stats')
@login_required
def api_quick_stats():
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Total launches this week
    total_launches = ToolUsage.query.filter(ToolUsage.timestamp >= seven_days_ago).count()
    
    # Most used tool this week
    most_used = db.session.query(
        Tool.display_name,
        func.count(ToolUsage.id).label('count')
    ).join(ToolUsage).filter(
        ToolUsage.timestamp >= seven_days_ago
    ).group_by(Tool.id).order_by(desc('count')).first()
    
    # Active users this week
    active_users = db.session.query(func.count(func.distinct(ToolUsage.user_id))).filter(
        ToolUsage.timestamp >= seven_days_ago
    ).scalar() or 0
    
    # Average daily usage
    unique_days = db.session.query(
        func.count(func.distinct(func.date(ToolUsage.timestamp)))
    ).filter(
        ToolUsage.timestamp >= seven_days_ago
    ).scalar() or 1
    
    avg_daily_usage = total_launches / unique_days
    
    return jsonify({
        'most_used_tool': most_used[0] if most_used else 'N/A',
        'most_used_count': most_used[1] if most_used else 0,
        'total_launches': total_launches,
        'active_users': active_users,
        'avg_daily_usage': round(avg_daily_usage, 1),
        'available_tools': Tool.query.filter_by(is_active=True).count()
    })
