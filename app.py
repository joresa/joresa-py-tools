"""
Dashboard application for joresa-py-tools
"""

from datetime import datetime, timedelta
import json
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Sample data for demonstration
TOOLS = [
    {
        "id": 1,
        "name": "Data Analyzer",
        "description": "Analyze and visualize data from various sources",
        "icon": "📊",
        "category": "Analytics",
        "launches": 145
    },
    {
        "id": 2,
        "name": "File Converter",
        "description": "Convert files between different formats",
        "icon": "🔄",
        "category": "Utilities",
        "launches": 89
    },
    {
        "id": 3,
        "name": "API Tester",
        "description": "Test and debug REST APIs",
        "icon": "🔧",
        "category": "Development",
        "launches": 234
    },
    {
        "id": 4,
        "name": "Report Generator",
        "description": "Generate automated reports from templates",
        "icon": "📄",
        "category": "Productivity",
        "launches": 178
    },
    {
        "id": 5,
        "name": "Database Manager",
        "description": "Manage and query databases",
        "icon": "🗄️",
        "category": "Database",
        "launches": 203
    },
    {
        "id": 6,
        "name": "Log Analyzer",
        "description": "Parse and analyze application logs",
        "icon": "📝",
        "category": "Monitoring",
        "launches": 112
    }
]


# Generate sample usage data for the past 7 days
def generate_usage_data():
    usage_data = []
    departments = ["Engineering", "Sales", "Marketing", "Operations", "HR"]
    users = ["alice@company.com", "bob@company.com", "charlie@company.com", 
             "diana@company.com", "eve@company.com", "frank@company.com"]
    
    for days_ago in range(7):
        date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        for tool in TOOLS:
            # Generate 5-15 usage events per tool per day
            import random
            random.seed(tool["id"] * 1000 + days_ago)
            num_events = random.randint(5, 15)
            for _ in range(num_events):
                usage_data.append({
                    "tool_id": tool["id"],
                    "tool_name": tool["name"],
                    "user": random.choice(users),
                    "department": random.choice(departments),
                    "timestamp": f"{date}T{random.randint(8,17):02d}:{random.randint(0,59):02d}:00",
                    "date": date
                })
    
    return usage_data


USAGE_DATA = generate_usage_data()


@app.route('/')
def dashboard():
    """Render the main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/tools')
def get_tools():
    """Get list of all available tools"""
    return jsonify(TOOLS)


@app.route('/api/analytics/top-tools')
def get_top_tools():
    """Get analytics for most used tools"""
    # Count usage by tool from past 7 days
    tool_usage = {}
    for usage in USAGE_DATA:
        tool_name = usage["tool_name"]
        tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1
    
    # Sort by usage count
    top_tools = sorted([{"name": name, "count": count} 
                       for name, count in tool_usage.items()],
                      key=lambda x: x["count"], reverse=True)
    
    return jsonify(top_tools)


@app.route('/api/analytics/timeline')
def get_timeline():
    """Get usage timeline data"""
    # Group by date
    timeline = {}
    for usage in USAGE_DATA:
        date = usage["date"]
        if date not in timeline:
            timeline[date] = 0
        timeline[date] += 1
    
    # Convert to sorted list
    timeline_data = [{"date": date, "count": count} 
                     for date, count in sorted(timeline.items())]
    
    return jsonify(timeline_data)


@app.route('/api/analytics/by-department')
def get_by_department():
    """Get usage by department"""
    dept_usage = {}
    for usage in USAGE_DATA:
        dept = usage["department"]
        dept_usage[dept] = dept_usage.get(dept, 0) + 1
    
    dept_data = [{"department": dept, "count": count} 
                 for dept, count in sorted(dept_usage.items(), 
                                          key=lambda x: x[1], reverse=True)]
    
    return jsonify(dept_data)


@app.route('/api/analytics/by-user')
def get_by_user():
    """Get usage by user"""
    user_usage = {}
    for usage in USAGE_DATA:
        user = usage["user"]
        user_usage[user] = user_usage.get(user, 0) + 1
    
    user_data = [{"user": user, "count": count} 
                 for user, count in sorted(user_usage.items(), 
                                          key=lambda x: x[1], reverse=True)]
    
    return jsonify(user_data)


@app.route('/api/analytics/quick-stats')
def get_quick_stats():
    """Get quick statistics"""
    # Most used tool this week
    tool_usage = {}
    for usage in USAGE_DATA:
        tool_name = usage["tool_name"]
        tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1
    
    most_used = max(tool_usage.items(), key=lambda x: x[1]) if tool_usage else ("N/A", 0)
    
    # Unique users
    unique_users = len(set(u["user"] for u in USAGE_DATA))
    
    # Average daily usage
    dates = set(u["date"] for u in USAGE_DATA)
    avg_daily = len(USAGE_DATA) / len(dates) if dates else 0
    
    # Total tool launches
    total_launches = len(USAGE_DATA)
    
    stats = {
        "most_used_tool": most_used[0],
        "most_used_count": most_used[1],
        "unique_users": unique_users,
        "avg_daily_usage": round(avg_daily, 1),
        "total_launches": total_launches,
        "active_tools": len(TOOLS)
    }
    
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
