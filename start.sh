#!/bin/bash

# Joresa Tools - Quick Start Script
# This script sets up and runs both backend and frontend

echo "🚀 Starting Joresa Tools..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Setup backend
echo "📦 Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt

# Start backend in background
echo "🔧 Starting backend server on http://localhost:8000..."
python main.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Setup frontend
echo "📦 Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi

# Start frontend in background
echo "🎨 Starting frontend on http://localhost:5173..."
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Joresa Tools is running!"
echo ""
echo "📊 Dashboard: http://localhost:5173"
echo "🔌 API: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services..."

# Trap Ctrl+C and cleanup
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT

# Wait for user interrupt
wait
