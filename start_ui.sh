#!/bin/bash

# Trace ID Helper Web UI Startup Script

echo "🔍 Starting Trace ID Helper Web UI..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3.6+ and try again."
    exit 1
fi

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing Flask dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install Flask. Please check your Python/pip installation."
        exit 1
    fi
fi

echo "✅ Dependencies are ready!"
echo ""
echo "🚀 Starting Flask web server..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 app.py