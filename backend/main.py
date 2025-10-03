"""
FastAPI backend for joresa-py-tools
Provides API endpoints for usage data and statistics
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random

app = FastAPI(title="Joresa Tools API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Joresa Tools API",
        "version": "1.0.0",
        "endpoints": ["/api/usage/daily", "/api/usage/summary"]
    }


@app.get("/api/usage/daily")
async def get_daily_usage():
    """Get daily usage statistics for the last 7 days"""
    data = []
    today = datetime.now()
    
    for i in range(7):
        date = today - timedelta(days=6 - i)
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "label": date.strftime("%a"),
            "requests": random.randint(100, 500),
            "users": random.randint(10, 50),
            "errors": random.randint(0, 10)
        })
    
    return {"data": data}


@app.get("/api/usage/summary")
async def get_usage_summary():
    """Get overall usage summary"""
    return {
        "total_requests": random.randint(5000, 10000),
        "total_users": random.randint(200, 500),
        "success_rate": round(random.uniform(95, 99.5), 2),
        "avg_response_time": round(random.uniform(50, 200), 2),
        "uptime_percentage": round(random.uniform(99.5, 99.99), 2)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
