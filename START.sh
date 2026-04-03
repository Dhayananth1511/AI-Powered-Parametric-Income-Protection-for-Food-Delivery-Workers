#!/bin/bash
# START_GIGSECURE.sh - Quick start script for GigSecure 2.1.0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛡️  GigSecure — AI-Powered Parametric Income Protection v2.1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.10+"
    exit 1
fi

echo "✅ Python available: $(python --version)"
echo ""

# Navigate to project directory
cd gigsecure

# Check if venv exists, else create it
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Starting GigSecure API..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the application
python main.py

# If the above fails, show error
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to start GigSecure"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check if requirements.txt installed successfully"
    echo "2. Check gigsecure.log for error details"
    echo "3. Ensure port 8000 is not already in use"
    echo ""
    exit 1
fi
