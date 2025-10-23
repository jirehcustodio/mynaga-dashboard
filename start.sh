#!/bin/bash

# MyNaga Dashboard - Easy Startup Script
# This script starts both backend and frontend servers

echo "🚀 Starting MyNaga Dashboard..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup INT TERM

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found!"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Frontend directory not found!"
    exit 1
fi

# Start backend
echo "📦 Starting backend server..."
cd "$BACKEND_DIR"
python3 -m uvicorn main:app --reload --app-dir "$BACKEND_DIR" > /tmp/mynaga-backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Backend logs: /tmp/mynaga-backend.log"
echo ""

# Wait for backend to start
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start! Check logs at /tmp/mynaga-backend.log"
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend server..."
cd "$FRONTEND_DIR"
npm run dev > /tmp/mynaga-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
echo "   Frontend logs: /tmp/mynaga-frontend.log"
echo ""

# Wait for frontend to start
sleep 3

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend failed to start! Check logs at /tmp/mynaga-frontend.log"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ MyNaga Dashboard is running!"
echo ""
echo "📍 Access your dashboard:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://127.0.0.1:8000"
echo "   API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "🔐 Your MyNaga Token:"
echo "   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2OGE0ODk3Zjg1ZmIxYTdiYjU2YTNjYTQiLCJpYXQiOjE3NjA1ODE1NDgsImV4cCI6MTc2MTE4NjM0OH0.AlIem843s3R_SaGLQVMjP3EfYaVMrOKANoVYv7zX3ns"
echo ""
echo "📝 Next steps:"
echo "   1. Open http://localhost:3000"
echo "   2. Click 'MyNaga Sync' in sidebar"
echo "   3. Paste your token"
echo "   4. Click 'Test Connection'"
echo "   5. Click 'Configure'"
echo "   6. Enjoy real-time sync! ⚡"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Keep script running
wait
